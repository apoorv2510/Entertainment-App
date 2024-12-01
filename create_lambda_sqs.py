import boto3
import zipfile
import io
import json

# AWS Configuration
AWS_REGION = "us-east-1"  # Replace with your region
LAMBDA_ROLE_ARN = "arn:aws:iam::381492313044:role/LabRole"  # Replace with your Lambda execution role ARN
LAMBDA_FUNCTION_NAME = "SQSLambdaProcessor"
LAMBDA_HANDLER = "lambda_function.lambda_handler"
QUEUE_NAME = "MySQSQueue"

# Lambda function code
LAMBDA_CODE = """
import json
import logging

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message_body = record['body']
            logging.info(f"Processing message: {message_body}")
        return {"statusCode": 200, "body": "Messages processed successfully"}
    except Exception as e:
        logging.error(f"Error processing messages: {e}")
        return {"statusCode": 500, "body": str(e)}
"""

def create_sqs_queue(queue_name):
    """Create an SQS queue."""
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    try:
        response = sqs_client.create_queue(QueueName=queue_name)
        queue_url = response['QueueUrl']
        print(f"SQS Queue created: {queue_url}")
        return queue_url
    except Exception as e:
        print(f"Error creating SQS queue: {e}")
        return None

def create_lambda_function():
    """Create a Lambda function."""
    lambda_client = boto3.client("lambda", region_name=AWS_REGION)

    # Create a ZIP package for the Lambda function
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("lambda_function.py", LAMBDA_CODE)
    zip_buffer.seek(0)

    try:
        response = lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime="python3.9",  # Adjust based on your preferred runtime
            Role=LAMBDA_ROLE_ARN,
            Handler=LAMBDA_HANDLER,
            Code={"ZipFile": zip_buffer.read()},
            Timeout=10,
            MemorySize=128,
        )
        print(f"Lambda function created: {response['FunctionArn']}")
        return response["FunctionArn"]
    except Exception as e:
        print(f"Error creating Lambda function: {e}")
        return None

def add_sqs_trigger_to_lambda(lambda_arn, queue_url):
    """Add the SQS queue as a trigger for the Lambda function."""
    lambda_client = boto3.client("lambda", region_name=AWS_REGION)
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)

    # Get the queue ARN
    try:
        queue_attributes = sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=['QueueArn']
        )
        queue_arn = queue_attributes['Attributes']['QueueArn']
    except Exception as e:
        print(f"Error retrieving queue ARN: {e}")
        return

    # Grant Lambda permissions to consume messages from the SQS queue
    try:
        lambda_client.add_permission(
            FunctionName=LAMBDA_FUNCTION_NAME,
            StatementId="SQSPermission",
            Action="lambda:InvokeFunction",
            Principal="sqs.amazonaws.com",
            SourceArn=queue_arn,
        )
        print("Permission added for Lambda to consume SQS messages")
    except Exception as e:
        print(f"Error adding permission: {e}")

    # Create the event source mapping
    try:
        response = lambda_client.create_event_source_mapping(
            EventSourceArn=queue_arn,
            FunctionName=LAMBDA_FUNCTION_NAME,
            BatchSize=10,  # Number of messages per batch
            Enabled=True,
        )
        print(f"SQS trigger added to Lambda: {response}")
    except Exception as e:
        print(f"Error creating event source mapping: {e}")

def main():
    # Step 1: Create the SQS queue
    queue_url = create_sqs_queue(QUEUE_NAME)
    if not queue_url:
        return

    # Step 2: Create the Lambda function
    lambda_arn = create_lambda_function()
    if not lambda_arn:
        return

    # Step 3: Add the SQS trigger to the Lambda function
    add_sqs_trigger_to_lambda(lambda_arn, queue_url)

if __name__ == "__main__":
    main()
