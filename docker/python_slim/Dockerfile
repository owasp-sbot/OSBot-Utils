# Stage 1: Build the wheel
FROM python:3.12.3-slim as builder

## Install dependencies for building
#RUN apt-get update && apt-get install -y build-essential

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy only the necessary files for building
COPY pyproject.toml poetry.lock* README.md ./

# Install project dependencies
RUN poetry install --only=main --no-root

# Copy the rest of the files
COPY ./osbot_utils ./osbot_utils

# Build the wheel
RUN poetry build -f wheel

# Stage 2: Create a minimal runtime image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy the wheel from the builder stage
COPY --from=builder /app/dist/*.whl .

# Install the wheel
RUN pip install ./*.whl

# Default command
CMD ["python", "-c", "from osbot_utils.utils.Dev import pprint; pprint('Hello from the container'); pprint('OSBot-Utils was installed ok')"]
