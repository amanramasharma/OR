# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the server and frontend site
COPY server/ ./server/
COPY public_site/ ./public_site/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the default FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]