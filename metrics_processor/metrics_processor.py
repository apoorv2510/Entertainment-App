import boto3
import zipfile
import io
import json
import os

AWS_REGION = "us-east-1"  # Replace with your AWS region
LAMBDA_ROLE_ARN = "arn:aws:iam::381492313044:role/LabRole"  # Replace with your Lambda execution role ARN
LAMBDA_FUNCTION_NAME = "MetricsProcessor"
LAMBDA_HANDLER = "metrics_processor.lambda_handler"
EVENT_RULE_NAME = "CPPpro123"
SCHEDULE_EXPRESSION = "rate(5 minutes)"  # Example: runs every 5 minutes

# Lambda function code as a Python script
LAMBDA_CODE = """
import json
import boto3

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    try:
        # Log the received event
        print(f"Received event: {json.dumps(event)}")
        
        # Example: Log a periodic metric to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='RealTimeMetrics',
            MetricData=[
                {
                    'MetricName': 'ScheduledTrigger',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
        return {"statusCode": 200, "body": "Metric logged successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": str(e)}
"""

def create_lambda_function():
    # Initialize the Lambda client
    lambda_client = boto3.client("lambda", region_name=AWS_REGION)
    
    # Create a ZIP package for the Lambda function
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("metrics_processor.py", LAMBDA_CODE)
    zip_buffer.seek(0)

    # Create the Lambda function
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

def create_cloudwatch_event_trigger(lambda_arn):
    # Initialize the EventBridge (CloudWatch Events) client
    events_client = boto3.client("events", region_name=AWS_REGION)
    
    # Create the CloudWatch Event Rule
    try:
        rule_response = events_client.put_rule(
            Name=EVENT_RULE_NAME,
            ScheduleExpression=SCHEDULE_EXPRESSION,
            State="ENABLED",
            Description="Trigger Lambda every 5 minutes",
        )
        rule_arn = rule_response["RuleArn"]
        print(f"Event rule created: {rule_arn}")
    except Exception as e:
        print(f"Error creating Event rule: {e}")
        return None

    # Add Lambda as a target for the rule
    try:
        events_client.put_targets(
            Rule=EVENT_RULE_NAME,
            Targets=[
                {
                    "Id": "1",
                    "Arn": lambda_arn,
                }
            ],
        )
        print("Added Lambda function as target for the Event rule")
    except Exception as e:
        print(f"Error adding Lambda function as target: {e}")
        return None

    # Grant EventBridge permission to invoke the Lambda function
    try:
        lambda_client = boto3.client("lambda", region_name=AWS_REGION)
        lambda_client.add_permission(
            FunctionName=LAMBDA_FUNCTION_NAME,
            StatementId="EventBridgeInvokePermission",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=rule_arn,
        )
        print("Granted EventBridge permission to invoke Lambda function")
    except Exception as e:
        print(f"Error granting permission to EventBridge: {e}")

def main():
    # Step 1: Create the Lambda function
    lambda_arn = create_lambda_function()
    if lambda_arn:
        # Step 2: Create the CloudWatch Event trigger
        create_cloudwatch_event_trigger(lambda_arn)

if __name__ == "__main__":
    main()
