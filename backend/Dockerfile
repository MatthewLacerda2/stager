FROM python:3.11-slim

# Install system dependencies including Blender and curl for healthchecks
RUN apt-get update && apt-get install -y \
    blender \
    curl \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements from root (assuming they are there as per list_dir)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set PYTHONPATH to include the root directory
ENV PYTHONPATH=/app

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
