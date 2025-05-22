# Use Python base image
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Copy entire project contents
COPY server/ server/
COPY public_site/ public_site/
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Change into server for runtime
WORKDIR /app/server

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
