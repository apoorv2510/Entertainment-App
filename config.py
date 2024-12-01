import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', '3306')  # Adding a default port for MySQL
}

# AWS S3 Configuration
AWS_S3_CONFIG = {
    'region': os.getenv('AWS_REGION'),
    'bucket_name': os.getenv('AWS_BUCKET_NAME'),
    'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
    'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'session_token': os.getenv('AWS_SESSION_TOKEN')  # Optional for temporary credentials
}

# AWS SNS Configuration
AWS_SNS_CONFIG = {
    'region': os.getenv('AWS_REGION'),
    'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
    'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'session_token': os.getenv('AWS_SESSION_TOKEN'),  # Optional for temporary credentials
    'topic_arn': os.getenv('AWS_SNS_TOPIC_ARN')  # ARN of the SNS topic
}

# AWS Lambda Configuration
AWS_LAMBDA_CONFIG = {
    'region': os.getenv('AWS_REGION'),
    'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
    'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'session_token': os.getenv('AWS_SESSION_TOKEN'),  # Optional for temporary credentials
    'function_name': os.getenv('AWS_LAMBDA_FUNCTION_NAME')  # Name of the Lambda function
}

# AWS SQS Configuration
AWS_SQS_CONFIG = {
    'region': os.getenv('AWS_REGION'),
    'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
    'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'session_token': os.getenv('AWS_SESSION_TOKEN'),  # Optional for temporary credentials
    'queue_url': os.getenv('AWS_SQS_QUEUE_URL')  # URL of the SQS queue
}

# Flask Application Configuration
FLASK_CONFIG = {
    'secret_key': os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
}

# General Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOGGING_LEVEL', 'INFO')  # Default log level
}

