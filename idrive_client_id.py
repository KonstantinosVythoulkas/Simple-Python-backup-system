import boto3
import os

endpoint = os.environ.get('IDRIVE_ENDPOINT')
access_key_id = os.environ.get('IDRIVE_ACCESSKEY')
secret_access_key = os.environ.get('IDRIVE_SECRETKEY')

session = boto3.session.Session()
idrive_client = session.client(
    service_name='s3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
)

def idrive_id():
    return idrive_client
