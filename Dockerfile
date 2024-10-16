# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /App
# Copy the current directory contents into the container at /app
COPY hello.py /App

# Run hello_world.py when the container launches
CMD ["python", "hello.py"]