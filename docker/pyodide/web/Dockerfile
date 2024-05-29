# Start with a base image with Nginx
FROM nginx:latest

# Create directory for app
RUN mkdir -p /usr/share/nginx/html/app

# Copy the static files into the container
COPY index.html         /usr/share/nginx/html/app
COPY simple-repl.js     /usr/share/nginx/html/app
COPY simple-repl.html   /usr/share/nginx/html/app

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d

# Expose the port Nginx is running on
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
