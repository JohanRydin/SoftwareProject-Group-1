# Use the ARM64 version of the Python 3.9 slim image
FROM arm64v8/python:3.10

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONBUFFERED 1 

WORKDIR /code 


# Install necessary system dependencies for ARM64 architecture
RUN apt-get update --fix-missing && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir /code/requirements.txt 


# Copy the requirements.txt file into the container
COPY ./requirements.txt /code/

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir --prefer-binary -r /code/requirements.txt

# Create a directory for your work files
RUN mkdir /workdir

# Copy the rest of the code into the container
COPY ./ /code/

# Run initialization script
RUN python /code/initialize.py

# Expose port for the FastAPI app
EXPOSE 5000

# Use Uvicorn to run the FastAPI application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]


