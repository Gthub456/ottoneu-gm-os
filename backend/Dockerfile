FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app/backend/app
COPY alembic /app/backend/alembic
COPY alembic.ini /app/backend/alembic.ini

# Default command
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]