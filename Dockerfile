# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client (optional, in case you need to access DB from the container)
RUN apt-get update && apt-get install -y postgresql-client

# Expose the port the Dash app will run on
EXPOSE 8050