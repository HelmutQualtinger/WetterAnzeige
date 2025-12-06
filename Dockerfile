# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install tzdata and set timezone to Europe/Zurich
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Zurich /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
ENV TZ=Europe/Zurich

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=600 --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "app.py"]
