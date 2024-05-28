# Use an official Node.js runtime as the base image
FROM node:20-alpine

# Create and set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose a port (optional, only if you plan to use a web server later)
EXPOSE 8080

# Command to run the Pyodide shell script
CMD ["node", "pyodide_shell.js"]
