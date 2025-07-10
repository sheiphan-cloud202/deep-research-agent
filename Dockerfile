# Use an official Astral uv image with Python 3.11 as a builder
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set up the working directory
WORKDIR /app

# Copy project definition files
COPY pyproject.toml uv.lock ./

# Create the package directory so uv can find the project. This is needed by `uv sync`.
RUN mkdir -p deep_research_agent

# Install all dependencies from pyproject.toml (including all extras) into a virtual environment.
# We use --no-install-project to prevent installing the local deep-research-agent package itself,
# allowing us to cache the third-party dependency layer separately from the application code.
RUN uv sync --all-extras --no-install-project

# Copy the rest of the application code
COPY deep_research_agent/ ./deep_research_agent
COPY lambda_function.py .

# --- Final Stage ---
# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory in the final image
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy dependencies from the builder stage's virtual environment.
# This copies the contents of site-packages directly into the Lambda runtime's path.
COPY --from=builder /app/.venv/lib/python3.11/site-packages/ .

# Copy application code from the builder stage
COPY --from=builder /app/deep_research_agent/ ./deep_research_agent
COPY --from=builder /app/lambda_function.py .

# Set the command to run the Lambda handler
CMD [ "lambda_function.lambda_handler" ]
