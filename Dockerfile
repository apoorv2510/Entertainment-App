# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (these will be passed during build time)
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN
ARG AWS_REGION
ARG AWS_BUCKET_NAME
ARG AWS_SNS_TOPIC_ARN
ARG AWS_SQS_QUEUE_URL
ARG LAMBDA_FUNCTION_NAME
ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG FLASK_SECRET_KEY

# Set default environment variables in the container
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
    AWS_REGION=$AWS_REGION \
    AWS_BUCKET_NAME=$AWS_BUCKET_NAME \
    AWS_SNS_TOPIC_ARN=$AWS_SNS_TOPIC_ARN \
    AWS_SQS_QUEUE_URL=$AWS_SQS_QUEUE_URL \
    LAMBDA_FUNCTION_NAME=$LAMBDA_FUNCTION_NAME \
    DB_HOST=$DB_HOST \
    DB_USER=$DB_USER \
    DB_PASSWORD=$DB_PASSWORD \
    DB_NAME=$DB_NAME \
    FLASK_SECRET_KEY=$FLASK_SECRET_KEY

# Expose the port the application runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


