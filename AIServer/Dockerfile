# Use the official Python image compatible with ARM64
FROM python:3.9-slim

# Set working directory
WORKDIR /code

# Install necessary build tools and libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    libopenblas-dev \
    && apt-get clean

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Preinstall dependencies
RUN pip install numpy cython

# Copy requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --use-deprecated=legacy-resolver
# Copy the rest of the application code
COPY . /code

# Set default command
CMD ["python3", "app.py"]
