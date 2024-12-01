import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class S3Client:
    def __init__(self):
        """
        Initializes the S3 client using credentials from .env.
        Validates the credentials and raises an error if invalid.
        """
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION')
            )
            self._validate_credentials()  # Validate credentials
        except Exception as e:
            raise Exception(f"Error initializing S3 client: {str(e)}")

    def _validate_credentials(self):
        """
        Validates the provided AWS credentials by attempting to list buckets.
        Raises an exception if credentials are invalid or permissions are insufficient.
        """
        try:
            self.s3_client.list_buckets()
        except boto3.exceptions.Boto3Error as e:
            raise Exception("Invalid AWS credentials or insufficient permissions.") from e

    def upload_file(self, file_obj, file_name):
        """
        Uploads a file to the S3 bucket.

        Args:
            file_obj: The file object to upload.
            file_name: The name to assign the file in the bucket.

        Returns:
            str: The URL of the uploaded file.
        """
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        try:
            self.s3_client.upload_fileobj(file_obj, bucket_name, file_name)
            file_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_name}"
            return file_url
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {str(e)}")

    def list_files(self):
        """
        Lists files in the S3 bucket.

        Returns:
            list: A list of file names in the bucket.
        """
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            return []
        except Exception as e:
            raise Exception(f"Error listing files in S3 bucket: {str(e)}")

    def delete_file(self, file_name):
        """
        Deletes a file from the S3 bucket.

        Args:
            file_name: The name of the file to delete.

        Returns:
            None
        """
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        except Exception as e:
            raise Exception(f"Error deleting file from S3 bucket: {str(e)}")
