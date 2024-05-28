FROM python:3.10.14-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY ./requirements-test.txt ./requirements-test.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy application code
COPY . .
RUN pip install -e .

# Command to run your tests
CMD ["pytest", "tests"]
