# Use an official Python runtime as the base image
FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
COPY ecommerce /app/
COPY manage.py /app/
COPY requirements.txt /app/
COPY static/ /app/
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
   build-essential \
   libpq-dev \
   && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
#COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
#COPY . /app/

# Copy the entrypoint script into the container and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port your app runs on (Django default is 8000)
EXPOSE 8000

# Set the entrypoint to the entrypoint script
#ENTRYPOINT ["/entrypoint.sh"]

