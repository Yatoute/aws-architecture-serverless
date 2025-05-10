#################################################################################################
##                                                                                             ##
##                                 NE PAS TOUCHER CETTE PARTIE                                 ##
##                                                                                             ##
## 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 ##
import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config
from botocore.exceptions import ClientError
import os
import uuid
from dotenv import load_dotenv
from typing import Union
import logging
from fastapi import FastAPI, Request, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from getSignedUrl import getSignedUrl
from posts_service import (
    get_user_posts, get_posts, create_presigned_url,
    get_post_by_id
)
load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logger.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Post(BaseModel):
    title: str
    body: str

my_config = Config(
    region_name='us-east-1',
    signature_version='v4',
)

dynamodb = boto3.resource('dynamodb', config=my_config)
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
bucket = os.getenv("BUCKET")

## ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ##
##                                                                                                ##
####################################################################################################




@app.post("/posts")
async def post_a_post(post: Post, authorization: str | None = Header(default=None)):
    """
    Poste un post ! Les informations du poste sont dans post.title, post.body et le user dans authorization
    """
    logger.info(f"title : {post.title}")
    logger.info(f"body : {post.body}")
    logger.info(f"user : {authorization}")
    
    post_id = f'{uuid.uuid4()}'
    
    try :
        res = table.put_item(
            Item = {
                "id": f"POST#{post_id}",
                "user" : f"USER#{authorization}",
                "title" : post.title,
                "body" : post.body
            }
        )  
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de validation des données : {str(e)}"
        )
       
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur inattendue : {str(e)}"
        )
        
    # Doit retourner le résultat de la requête la table dynamodb
    return JSONResponse(content=res, status_code=res["ResponseMetadata"]["HTTPStatusCode"])

@app.get("/posts")
async def get_all_posts(user: Union[str, None] = None):
    """
    Récupère tout les postes. 
    - Si un user est présent dans le requête, récupère uniquement les siens
    - Si aucun user n'est présent, récupère TOUS les postes de la table !!
    """  
    if user :
        posts = get_user_posts(user)
    else :
        posts = get_posts()
    
    items = posts["Items"]

    # Créer des urls signés pour les images jointes aux posts
    for item in items:
        image = item.get("image", None)
        if image :
            item["image"] = create_presigned_url(
                bucket_name=bucket, 
                object_name=image
            )
           
     # Doit retourner une liste de posts
    return JSONResponse(content=items, status_code=posts["ResponseMetadata"]["HTTPStatusCode"])

    
@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, authorization: str | None = Header(default=None)):
    # Doit retourner le résultat de la requête la table dynamodb
    logger.info(f"post id : {post_id}")
    logger.info(f"user: {authorization}")
    # Récupération des infos du poste
    post = get_post_by_id(authorization, post_id)
        
    if len(post["Items"])==0:
        res = "Ce post n'existe peut être pas ou vous n'est pas autorisé à le supprimer."
        return JSONResponse(content=res)
    
    image = post["Items"][0].get("image", None)
    try:
        # S'il y a une image on la supprime de S3
        if image:
            s3_client.delete_object(Bucket= bucket, Key=image)
            
        # Suppression de la ligne dans la base dynamodb
            res = table.delete_item(
                Key = {
                    "user": f"USER#{authorization}",
                    "id": f"POST#{post_id}"
                }
            )
    except ClientError as e:
        raise HTTPException(
            status_code= e.response['ResponseMetadata']['HTTPStatusCode'],
            detail= e.response['Error']['Message']
        )
   
    # Retourne le résultat de la requête de suppression
    return JSONResponse(content=res, status_code=res["ResponseMetadata"]["HTTPStatusCode"])



#################################################################################################
##                                                                                             ##
##                                 NE PAS TOUCHER CETTE PARTIE                                 ##
##                                                                                             ##
## 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 ##
@app.get("/signedUrlPut")
async def get_signed_url_put(filename: str,filetype: str, postId: str,authorization: str | None = Header(default=None)):
    return getSignedUrl(filename, filetype, postId, authorization)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="debug")

## ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ☝️ ##
##                                                                                                ##
####################################################################################################