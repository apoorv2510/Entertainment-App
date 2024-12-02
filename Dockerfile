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

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV AWS_ACCESS_KEY_ID="ASIAVRUVWXPKA55EDI3Y"
ENV AWS_SECRET_ACCESS_KEY="/u9Jnta1s91SYsT1OMb3btYjfSDTWmi45gfL18dJ"
ENV AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEAgaCXVzLXdlc3QtMiJGMEQCIHwDzS4xy7O0egp4K/N9cGrMJCcPvc8su9crnnYTG6JRAiBg8uqTA1m+0IE8qydxSyJDYm+FOSEiOQOWPpSzG5xBByq9Agix//////////8BEAAaDDM4MTQ5MjMxMzA0NCIMrZj2shsOxnEO8HyCKpEC7KkdspTQNZYtsWtyXvZHzwWWjc3t9/BITkLr2AqtYVGU7mE2Y+yci332rA/2gAs657Pnk7bVmD2xKEG7ePEpNckUyU4Jfm2nF6/GzeYkLZHtwkUg4LIBQonLfW5WC9FafCQ2hebF1DICUAc0soGFttWSACHu8F+psjlZ/W7uk4XiZ7Y/97PIwOFw2EWNfX1hXSc3uptmv7TbDs9F4/fR+fKJKSBMOq/zrb6sbsbrEkuWOW/GGaAXxcXsd7hbGvGCclbrvRLUdaq8A57ICkRHRdpiajTro0kxQ5upwpNVw7eYanAEuW2s27WnobFFgmuomqemG3jjHv9vMTKAzNY2+hc+DHjIu/kCIoRdOaXVkMmaMOfms7oGOp4BotteseAbPZNA6uIrwc8nVefu2vTcu2JnJIvOM1sMv/6wyumrQx738M+ivfkxHBr/XrI4k/u6YF4FcEqbigBZNMPlmQo1DqxEnVM5AlXdkswp1Hc47nnc97773dXR+y5bz80kljLFa8/RQgXOEQQxIMsGkhEgyz7mIvLWIt0Ft7M+mA07gcb/oa/VkMVDe4geNVf+JKSRQZ8rDVlTJVg="
ENV AWS_REGION="us-east-1"
ENV AWS_BUCKET_NAME="entertainment-hub-images"
ENV DB_HOST="entertainmentdb1.cx4ogu6mk4t6.us-east-1.rds.amazonaws.com"
ENV DB_USER="admin"
ENV DB_PASSWORD="password123"
ENV DB_NAME="entertainmentdb1"
ENV FLASK_SECRET_KEY="your_secret_key"
ENV AWS_SNS_TOPIC_ARN="arn:aws:sns:us-east-1:381492313044:entertainment-updates"
ENV AWS_SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/381492313044/MySQSQueue"
ENV LAMBDA_FUNCTION_NAME="MetricsProcessor"

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "application.py"]

