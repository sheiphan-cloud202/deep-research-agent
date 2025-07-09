# Use an official Astral uv image with Python 3.11 as a builder
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set up the working directory
WORKDIR /app

# Copy project files needed for dependency resolution
COPY pyproject.toml uv.lock ./

# Install dependencies only (not the project itself) for better Docker layer caching
RUN uv sync --locked --no-install-project --no-dev

# Copy the rest of the application code
COPY deep_research_agent/ ./deep_research_agent/
COPY lambda_function.py ./

# Now install the project itself in non-editable mode
RUN uv sync --locked --no-dev --no-editable

# --- Final Stage ---
# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory in the final image
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the complete virtual environment from the builder stage
COPY --from=builder /app/.venv/lib/python3.11/site-packages/ ./

# Copy application code from the builder stage
COPY --from=builder /app/deep_research_agent/ ./deep_research_agent/
COPY --from=builder /app/lambda_function.py ./

# Set the Lambda handler
CMD ["lambda_function.lambda_handler"]
