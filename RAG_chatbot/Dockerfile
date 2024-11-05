# Start from the NVIDIA CUDA runtime image
FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04
FROM python:3.11-bookworm
# Install Python and necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev python3-venv ca-certificates && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements file to install Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -U bitsandbytes
# Copy application files, including .env if needed
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
