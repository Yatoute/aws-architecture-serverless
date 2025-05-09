import json
from urllib.parse import unquote_plus
import boto3
import os
import logging
print('Loading function')
logger = logging.getLogger()
logger.setLevel("INFO")
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
reckognition = boto3.client('rekognition')

region = os.getenv('AWS_REGION')
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
bucket = os.getenv("BUCKET")


def lambda_handler(event, context):
    
    logger.info(json.dumps(event, indent=2))
    
    # Récupération du nom du bucket
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    
    # Récupération du nom de l'objet
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    
    # extration de l'utilisateur et de l'id de la tâche
    user, task_id = key.split('/')[:2]

    # Ajout des tags user et task_uuid
    user = f"USER#{user}"
    task_id = f"POST#{task_id}"
    
    # Appel à reckognition
    label_data = reckognition.detect_labels( 
        Image={
        "S3Object": {
        "Bucket": bucket,
        "Name": key
        }
        },
        MaxLabels=5,
        MinConfidence=0.75
    )
    logger.info(f"Labels data : {label_data}")
    
    # Récupération des résultats des labels
    labels = [label["Name"] for label in label_data["Labels"]]
    logger.info(f"Labels detected : {labels}")

    # Mise à jour de la table dynamodb
    table.update_item(
        Key = {
            "user": user,
            "id": task_id
            
        },
        UpdateExpression = "SET image = :img_key, label = :img_labels",
        ExpressionAttributeValues = {
            ":img_key": key, 
            ":img_labels": labels
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps("Tous les messages sont traités")
    }