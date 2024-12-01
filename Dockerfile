# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /usr/src/app

# Create app directory
WORKDIR $APP_HOME

# Copy application files to the container
COPY . $APP_HOME/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port
EXPOSE 5000

# Start the Flask application
CMD ["python", "application.py"]
