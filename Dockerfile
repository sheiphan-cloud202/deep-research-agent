# Use an official Astral uv image with Python 3.11 as a builder
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set up the working directory
WORKDIR /app

# Copy project definition files
COPY pyproject.toml uv.lock ./

# Create an empty directory for the local package.
# This is necessary because `uv` with a `pyproject.toml` present
# expects the package directory to exist, even if we're not installing it yet.
# We create it empty to avoid busting the cache on code changes.
RUN mkdir -p deep_research_agent

# Install third-party dependencies into a target directory for the Lambda environment
# We use `uv pip install .` to have `uv` resolve dependencies from `pyproject.toml` and `uv.lock`,
# but we exclude the project itself with `--exclude .` to only install third-party packages.
RUN uv pip install --no-cache --target /app/packages -e . --exclude .

# Copy the rest of the application code
COPY deep_research_agent/ ./deep_research_agent
COPY lambda_function.py .

# --- Final Stage ---
# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory in the final image
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy dependencies from the builder stage
COPY --from=builder /app/packages ./

# Copy application code from the builder stage
COPY --from=builder /app/deep_research_agent/ ./deep_research_agent
COPY --from=builder /app/lambda_function.py .

# Set the command to run the Lambda handler
CMD [ "lambda_function.lambda_handler" ]
