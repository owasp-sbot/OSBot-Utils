# Dockerfile for Python 3.10.14
FROM python:3.10.14-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements-test.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy application code
COPY . .

# Command to run your tests
CMD ["pytest", "tests"]
