# Base Image
FROM python:3.10-slim

# Set environment variables to ensure Python runs optimally
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure Python output is displayed in real-time

# Set working directory
WORKDIR /fastAPI

# Install system dependencies, including cryptography
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    build-essential \
    python3-dev \
    cargo \
    python3-cryptography \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies, excluding cryptography
COPY requirements.txt .
RUN sed -i '/cryptography/d' requirements.txt  # Remove 'cryptography' from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
