# Use the official Ubuntu image as the base image
FROM fedora:latest

# Set the working directory
WORKDIR /app

#UNCOMMENT FOR DEBUGGING
RUN #dnf install -y nano net-tools

# Start cron and keep the container running
CMD ["tail", "-f", "/dev/null"]
