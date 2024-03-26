# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow communication to the Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "server.py"]
