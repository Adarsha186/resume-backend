# Use the official Python image.
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Cloud Run expects the application to listen on
EXPOSE 8080

# Command to run your Flask app
CMD ["python", "main.py"]
