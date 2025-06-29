# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY graph-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY graph-service/. .
COPY common ./common
RUN chmod +x /app/common/scripts/wait-for-it.sh

# Run the main script
CMD ["python", "main.py"]
