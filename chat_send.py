import os
import time
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

# Load variables from .env in 'vars' directory
load_dotenv('vars/variables.env')

# Get environment variables
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
RASP_ID = os.getenv("RASP_ID")
WAIT_FOR_UPLOAD = int(os.getenv("WAIT_FOR_UPLOAD"))
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)

def upload_to_s3(local_file, s3_folder):
    try:
        s3.upload_file(local_file, BUCKET_NAME, s3_folder)
        print(f"Upload Successful for {local_file} to {s3_folder}")
        # Delete the file after successful upload
        os.remove(local_file)
        print(f"Local file {local_file} deleted")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def check_and_upload():
    # Loop through all files in the UPLOAD_FOLDER
    for file_name in os.listdir(UPLOAD_FOLDER):
        local_file = os.path.join(UPLOAD_FOLDER, file_name)
        
        # Parse the date from the file name and create the S3 folder structure
        date_str = file_name.split('_')[0]  # Assuming date is the first part split by '_'
        year, month, day = date_str[:4], date_str[4:6], date_str[6:8]
        
        # Construct the S3 path with "rngs", RASP_ID and the date
        s3_folder = '/'.join(['rngs', RASP_ID, year, month, day, file_name])
        
        # Upload file to S3
        upload_to_s3(local_file, s3_folder)

def run_continuously():
    while True:
        print("Checking for files to upload...")
        check_and_upload()
        print(f"Sleeping for {WAIT_FOR_UPLOAD} seconds...")
        time.sleep(WAIT_FOR_UPLOAD)

if __name__ == '__main__':
    run_continuously()
