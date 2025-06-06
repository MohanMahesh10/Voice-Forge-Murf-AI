FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for scipy, numpy, and pydub
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    ffmpeg \
    libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt azure-storage-blob cloudinary

# Copy all application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs

EXPOSE 8000

# Development command with reload
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production command without reload and with 4 workers for better performance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
