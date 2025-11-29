# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager itself, and kaggle
RUN pip install --no-cache-dir uv kaggle

# Copy pyproject.toml and uv.lock first (for layer caching)
COPY pyproject.toml uv.lock .python-version ./

# Install Python dependencies
RUN uv sync

# Copy application code
COPY ./main ./main

# Configuring Kaggle
RUN mkdir -p /root/.config/kaggle

# Download the finetuned models
RUN --mount=type=secret,id=env \
    export $(cat /run/secrets/env | xargs) && \
    uv run -m main download models FINETUNED

# Expose port
EXPOSE 8136

# Run the RPC server
CMD ["uv", "run", "-m", "main", "serve", "--host", "0.0.0.0", "--port", "8136"]
