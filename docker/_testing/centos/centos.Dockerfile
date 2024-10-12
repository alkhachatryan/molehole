# Use the official Ubuntu image as the base image
FROM centos:latest

# Set the working directory
WORKDIR /app

#UNCOMMENT FOR DEBUGGING
#RUN cd /etc/yum.repos.d/
#RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
#RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
#RUN yum install -y nano net-tools

# Start cron and keep the container running
CMD ["tail", "-f", "/dev/null"]
