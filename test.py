from dotenv import load_dotenv
import os
import boto3

# Load environment variables from .env file
load_dotenv()

# Access environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
aws_default_region = os.getenv("AWS_DEFAULT_REGION")

# Initialize AWS services with these credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

sts_client = session.client('sts')

# Test the credentials
try:
    identity = sts_client.get_caller_identity()
    print("Caller Identity:", identity)
except Exception as e:
    print(f"Error: {e}")
