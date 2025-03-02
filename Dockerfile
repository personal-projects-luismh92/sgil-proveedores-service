# Use official Python image
FROM python:3.11-alpine

# Install system dependencies required for psutil and other packages
RUN apk add --no-cache git gcc musl-dev python3-dev libffi-dev curl

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]
