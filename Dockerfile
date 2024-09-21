# Use the official Python base image
FROM python:3.12.0-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command for the container
CMD ["python3", "app.py"]
