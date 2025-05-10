import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config
from botocore.exceptions import ClientError
import os

import logging

my_config = Config(
    region_name='us-east-1',
    signature_version='v4',
)

dynamodb = boto3.resource('dynamodb', config=my_config)
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
bucket = os.getenv("BUCKET")

def get_user_posts(user: str):
    """Récupération des postes de l'utilisateur"""
    
    logger.info(f"Récupération des postes de : {user}")
    try:
        posts = table.query(
            Select = 'ALL_ATTRIBUTES',
            KeyConditionExpression= Key("user").eq(f"USER#{user}")
        )
    except ClientError as e:
        logging.error(e)
        return None
    return posts
    
def get_all_posts():
    """Récupération de tous les postes"""
    
    logger.info("Récupération de tous les postes")
    try:
        posts = table.scan(
            Select = 'ALL_ATTRIBUTES'
        )
    except ClientError as e:
        logging.error(e)
        return None
    return posts

def get_post_by_id(user:str, post_id:str):
    """Récupérer un post par son PK et SK"""
    
    try :
        post =  table.query(
            Select = 'ALL_ATTRIBUTES',
            KeyConditionExpression= Key("user").eq(f"USER#{user}") & Key("id").eq(f"POST#{post_id}")
        )
   except ClientError as e:
        logging.error(e)
        return None
    
    return post

def create_presigned_url(bucket_name:str, object_name:str, expiration:int =3600):
    """Generate a presigned URL to share an S3 object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response