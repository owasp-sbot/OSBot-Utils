# Use the official Python image with Python 3.12.2
FROM python:3.12.2-slim

# Install OpenSSH server and necessary utilities
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    mkdir -p /root/.ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add a custom .bashrc to log interactive commands
RUN echo 'export PROMPT_COMMAND="history -a; echo \$(date) \$(whoami) \$(history 1 | sed \"s/^[ ]*[0-9]*[ ]*//\") >> /var/log/commands.log"' >> /root/.bashrc

# Add a script to log non-interactive commands
RUN echo '#!/bin/bash\n\
echo "$(date) $(whoami) $SSH_ORIGINAL_COMMAND" >> /var/log/commands.log\n\
exec $SSH_ORIGINAL_COMMAND' > /usr/local/bin/log_command.sh && \
chmod +x /usr/local/bin/log_command.sh

# Configure SSH to use the script for non-interactive sessions
RUN echo 'ForceCommand /usr/local/bin/log_command.sh' >> /etc/ssh/sshd_config

# Create a script to set up the authorized_keys from an environment variable
RUN echo '#!/bin/bash\n\
echo "$AUTHORIZED_KEYS" > /root/.ssh/authorized_keys\n\
chmod 600 /root/.ssh/authorized_keys\n\
touch /var/log/commands.log\n\
tail -f /var/log/commands.log &\n\
exec /usr/sbin/sshd -D' > /start.sh && \
chmod +x /start.sh

# Expose SSH port
EXPOSE 22

# Start the SSH service via the start script
CMD ["/start.sh"]
