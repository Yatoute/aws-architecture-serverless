import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv
load_dotenv("../webservice/.env")
from data import data

bucket = os.getenv("BUCKET")
table_name = os.getenv("DYNAMO_TABLE")
s3 = boto3.resource('s3')
my_config = Config(
    region_name='us-east-1',
    signature_version='v4',
)
dynamodb = boto3.resource('dynamodb', config=my_config)

# Les posts
# Get the table.
table = dynamodb.Table(table_name)
# Read file
with table.batch_writer() as batch:
    for row in data:
        batch.put_item(Item=row)

# Uploader les images jointes au posts
for (dirpath, dirnames, filenames) in os.walk("s3"):
    if filenames:
        for filename in filenames:
            with open(f"{dirpath}/{filename}", 'rb') as file:
                s3.Object(bucket, f"{'/'.join(dirpath.split(os.path.sep)[1:])}/{filename}").put(Body=file)
          
