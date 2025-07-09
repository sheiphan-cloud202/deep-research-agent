# Use an official Astral uv image with Python 3.11 as a builder
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Set up the working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./

# Export dependencies from the lock file to requirements.txt
RUN uv export --frozen --no-dev --no-editable --all-extras -o requirements.txt

# Remove the local package from the requirements file. This allows us to cache
# the installation of third-party dependencies in a separate Docker layer.
# Local packages are identified by 'file:///' in the requirements.txt.
RUN grep -v "file:///" requirements.txt > requirements.tmp && mv requirements.tmp requirements.txt

# Install third-party dependencies into a target directory for the Lambda environment
RUN uv pip install --no-cache -r requirements.txt --target /app/packages

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
