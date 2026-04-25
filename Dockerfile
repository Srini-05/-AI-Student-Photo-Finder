# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies needed for dlib and opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
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
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
