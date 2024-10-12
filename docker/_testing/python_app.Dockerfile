# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app


RUN apt update && apt install binutils iputils-ping -y

COPY ../../ .
RUN pip install -r requirements.txt

CMD ["sh", "-c", "pyinstaller server.spec && tail -f /dev/null"]
