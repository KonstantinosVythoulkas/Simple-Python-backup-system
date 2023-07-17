import boto3
import os

endpoint = os.environ.get('SYNOLOGY_ENDPOINT')
access_key_id = os.environ.get('SYNOLOGY_KEY')
secret_access_key = os.environ.get('SYNOLOGY_SECRET')

session = boto3.session.Session()
client = session.client(
    service_name='s3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    )

def synology_id():
    return client