# Lightweight Dockerfile for the Revyena bot
# Uses a slim Python image and installs requirements during build
FROM python:3.13-slim

# Ensure output is logged immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps required by some packages (asyncpg may need libpq-dev)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd -m appuser

# Copy application code
COPY . /app
RUN chown -R appuser:appuser /app
RUN pip install --no-cache-dir -r requirements.txt

USER appuser

# Default command (can be overridden by docker-compose)
CMD ["python", "main.py"]

