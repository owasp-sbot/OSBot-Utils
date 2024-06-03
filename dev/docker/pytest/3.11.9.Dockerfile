# Dockerfile for Python 3.11.9
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements-test.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy application code
COPY . .
RUN pip install -e .

# Command to run your tests
CMD ["pytest", "tests"]
