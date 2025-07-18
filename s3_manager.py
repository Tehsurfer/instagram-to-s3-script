import os
import boto3
import requests
from dotenv import load_dotenv

class S3Manager:
    def __init__(self, bucket_name):
        # Load environment variables from .env.local first, then .env
        load_dotenv('.env.local', override=True)
        load_dotenv('.env', override=False)

        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = os.getenv('AWS_REGION', 'ap-southeast-2')

        print(f"Using AWS_ACCESS_KEY_ID: {aws_access_key}")
        print(f"Using AWS_SECRET_ACCESS_KEY: {aws_secret_key}")
        print(f"Using AWS_REGION: {region_name}")

        if not aws_access_key or not aws_secret_key:
            raise ValueError("Missing AWS credentials in .env.local or .env file")

        self.s3 = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name
        self.folder = None  # Placeholder for folder if needed

    def set_folder(self, folder_name):
        """Set the folder path for uploads."""
        if not folder_name.endswith('/'):
            folder_name += '/'
        self.folder = folder_name
        print(f"Folder set to: {self.folder}")

    def upload_file(self, file_path, object_name=None):
        """Upload a file to an S3 bucket."""
        if object_name is None:
            object_name = file_path.split('/')[-1]
        self.s3.upload_file(file_path, self.bucket_name, object_name)

    def download_file(self, object_name, file_path):
        """Download a file from an S3 bucket."""
        self.s3.download_file(self.bucket_name, object_name, file_path)

    def list_files(self):
        """List files in the S3 bucket."""
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        return [item['Key'] for item in response.get('Contents', [])]

    def create_folder(self, folder_name):
        """Create a folder in the S3 bucket by uploading an empty object with trailing slash."""
        try:
            # Ensure folder name ends with a slash
            if not folder_name.endswith('/'):
                folder_name += '/'
            
            # Create an empty object to represent the folder
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=folder_name,
                Body=b''
            )
            print(f"Created folder: {folder_name} in bucket {self.bucket_name}")
            self.folder = folder_name  # Store the folder path if needed
            return f"s3://{self.bucket_name}/{folder_name}"
        except Exception as e:
            raise Exception(f"Error creating folder {folder_name}: {str(e)}")

    def upload_image_from_url(self, image_url, content_type="image/jpeg", object_name=None):
        return self.upload_file_from_url(image_url, content_type, object_name)

    def upload_video_from_url(self, video_url, content_type="video/mp4", object_name=None):
        return self.upload_file_from_url(video_url, content_type, object_name)

    def upload_file_from_url(self, file_url, content_type, object_name=None):
        """Download a file from a URL, upload it to S3, and return a permalink."""
        try:
            # Check file size first
            file_size = self.get_file_size_from_url(file_url)
            if file_size:
                print(f"File size: {file_size} bytes ({self.convert_bytes_to_mb(file_size):.2f} MB)")

            # Download the file
            response = requests.get(file_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download file from {file_url}: {response.status_code}")

            file_data = response.content

            # Determine object name
            object_name = self.process_file_name(file_url, object_name)
            
            # Add folder prefix if specified
            if self.folder:
                if not self.folder.endswith('/'):
                    self.folder += '/'
                object_name = self.folder + object_name

            # Check all vars
            print(f"Uploading {object_name} to bucket {self.bucket_name}, region {self.s3.meta.region_name}, data is {len(file_data)} bytes long")

            # Upload to S3 with metadata for inline display
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_data,
                ContentType=content_type,
                ContentDisposition='inline'
            )

            # Generate permalink
            s3_url = f"https://{self.bucket_name}.s3.{self.s3.meta.region_name}.amazonaws.com/{object_name}"
            return {
                "permalink": s3_url,
                "file_size": self.convert_bytes_to_mb(file_size) if file_size else None
            }
        except Exception as e:
            raise Exception(f"Error uploading image to S3: {str(e)}")
    
    @staticmethod
    def get_file_size_from_url(file_url):
        """Get the file size from a URL without downloading the file."""
        try:
            response = requests.head(file_url)
            if response.status_code == 200:
                content_length = response.headers.get('Content-Length')
                if content_length:
                    return int(content_length)
            return None
        except Exception as e:
            print(f"Could not get file size for {file_url}: {e}")
            return None
    
    @staticmethod
    def process_file_name(file_url, object_name=None):
        """Process the image name from the URL."""

        # if no object_name is provided, use the last part of the URL
        if object_name is None:
            object_name = file_url.split('/')[-1]
            if '?' in object_name:
                object_name = object_name.split('?')[0]
            return object_name

        # If object_name is provided, ensure it has the correct extension
        else:
            # Extract file extension from URL
            url_filename = file_url.split('/')[-1]
            if '?' in url_filename:
                url_filename = url_filename.split('?')[0]
            
            # Get extension from URL
            if '.' in url_filename:
                extension = '.' + url_filename.split('.')[-1]
                # Add extension to object_name if it doesn't already have one
                if not object_name.endswith(extension) and '.' not in object_name:
                    object_name += extension
            
            return object_name

    @staticmethod
    def convert_bytes_to_mb(byte_size):
        """Convert bytes to megabytes."""
        return byte_size / (1024 * 1024) if byte_size else 0

