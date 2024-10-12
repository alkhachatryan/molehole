# Use the official Ubuntu image as the base image
FROM debian:latest

# Set the working directory
WORKDIR /app

#UNCOMMENT FOR DEBUGGING
RUN #apt update && apt install -y nano net-tools

# Start cron and keep the container running
CMD ["tail", "-f", "/dev/null"]
