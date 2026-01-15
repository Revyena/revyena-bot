# Python 3.11 slim base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for asyncpg (libpq)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Default command to run the bot
CMD ["python", "-u", "main.py"]

