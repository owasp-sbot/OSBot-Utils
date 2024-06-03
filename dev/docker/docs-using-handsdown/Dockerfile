# Dockerfile
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install handsdown mkdocs mkdocs-material

# Make port 8000 available to the world outside this container
EXPOSE 8000
