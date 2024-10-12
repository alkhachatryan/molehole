# Use the official Ubuntu image as the base image
FROM archlinux:latest

# Set the working directory
WORKDIR /app

#UNCOMMENT FOR DEBUGGING
RUN #pacman -Sy --noconfirm nano net-tools

# Start cron and keep the container running
CMD ["tail", "-f", "/dev/null"]
