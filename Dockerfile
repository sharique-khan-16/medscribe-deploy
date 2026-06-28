# Use official python slim image
FROM python:3.11-slim

# Install system dependencies (including tesseract-ocr and opencv dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy source code and files
COPY src/ ./src/
COPY data/samples/ ./data/samples/
COPY tests/ ./tests/
COPY cliff.toml USER_MANUAL.md ./

# Expose FastAPI server port
EXPOSE 8000

# Set environment variable
ENV PYTHONPATH=/app

# Command to run backend
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]