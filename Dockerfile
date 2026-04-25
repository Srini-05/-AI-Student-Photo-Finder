# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies needed for dlib and opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p final_year graduation output unknown

# Expose the port
EXPOSE 8080

# Start the application with gunicorn for production performance
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app:app"]
