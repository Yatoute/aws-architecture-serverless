import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config

import os
from dotenv import load_dotenv
import uuid

load_dotenv()

my_config = Config(
    region_name='us-east-1',
    signature_version='v4',
)
dynamodb = boto3.resource('dynamodb', config=my_config)
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
bucket = os.getenv("BUCKET")

# print(bucket)
# s3= boto3.resource("s3")
# s3.Object(bucket, "Link/dfe03fe8-8eb0-4060-ab44-3be4ab9db2d5/103dbabe-cdbc-4477-98c6-596cd05329f0yor-forger.jpg").put(Body=".\init_data\s3\Anya\dfe03fe8-8eb0-4060-ab44-3be4ab9db2d5\103dbabe-cdbc-4477-98c6-596cd05329f0yor-forger.jpg")

## POST Posts
# res = table.put_item(
#     Item = {
#         "id": f"POST#{uuid.uuid4()}",
#         "user": f"USER#yatoute",
#         "title": "Bandes d'idiots",
#         "body": "Bandes d'idiots"
#     }
# )

# print(res)

## GET Posts
### Utilisateur : yatoute
# res = table.query(
#     Select = "ALL_ATTRIBUTES",
#     KeyConditionExpression = Key("user").eq("USER#yatoutes")
# )
# print(res)

### Utilisateur anonym
# res = table.scan(
#     Select = "ALL_ATTRIBUTES"
# )
# print(res)

## DELETE Posts
post =  table.query(
        Select = 'ALL_ATTRIBUTES',
        KeyConditionExpression= Key("user").eq(f"USER#Yatoute") & Key("id").eq("POST#48d6fb25-0685-4236-bf21-477aa7e66023")
    )
print(post)
if len(post["Items"])==0:
        res = "Ce post n'existe peut être pas ou vous n'est pas autorisé à le supprimer."
        print(res)
# S'il y a une image on la supprime de S3
# image = post["Items"][0].get("image", None)
# if image:
#     s3_client.delete_object(Bucket= bucket, Key=image)

# # Suppression de la ligne dans la base dynamodb
# res = table.delete_item(
#     Key = {
#         "user": f"USER#Anya",
#         "id": f"POST#899dd7d2-6935-47cd-accb-e9833530a24a"
#     }
# )
# print(res)