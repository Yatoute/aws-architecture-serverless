import uuid
import os
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("BUCKET")

data = [
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Anya',
        'title': 'La tueuse en mission',
        'body': 'Personne ne m’échappera ce soir...',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Anya/e785e61b-91a9-41fc-ad07-eebbef55cb2b/990e5717-a1c1-4caa-8beb-5ae28c2ef462yor+asssassin.jpg',
        'label': ['spyxfamily', 'assassine', 'yor']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Anya',
        'title': 'Routine de ménage',
        'body': 'Une maison propre, une double vie bien rangée !',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Anya/dfe03fe8-8eb0-4060-ab44-3be4ab9db2d5/103dbabe-cdbc-4477-98c6-596cd05329f0yor-forger.jpg',
        'label': ['spyxfamily', 'ménage', 'yor']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Deku',
        'title': 'Je suis là ! 💥',
        'body': 'Même dans l’ombre, je brillerai pour protéger les innocents.',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Deku/60888533-cc26-4e59-93ab-6964850ed447/ec3cd817-4655-4e30-9f90-860f716bc7b1all+might.jpeg',
        'label': ['mha', 'allmight', 'hero']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Link',
        'title': 'Face au Lynel doré',
        'body': 'Chaque combat est une épreuve de courage.',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Link/28d5598c-c699-4c9b-ab7b-0a0d921b1583/fb85dfdb-c0e9-4fd5-b2da-832610e00303lynel.jpg',
        'label': ['zelda', 'bossfight', 'lynel']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Link',
        'title': 'Épée légendaire',
        'body': 'La lame du héros est à nouveau entre mes mains.',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Link/915d2d13-cea2-4b80-8c5b-e90295b16876/1ce475b3-af6f-4c3b-b31c-d3acc2379ebcmaster+sword.jpeg',
        'label': ['zelda', 'master_sword', 'hero']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Setsuna',
        'title': 'GNT-0000 prêt au combat',
        'body': 'L’univers est vaste, mais mon devoir est clair.',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Setsuna/48d6fb25-0685-4236-bf21-477aa7e66023/f9547e91-431e-425a-894f-e55224c7ef92gundam+quanT.jpg',
        'label': ['gundam', 'mecha', 'spatial']
    },
    {
        'id': f'POST#{uuid.uuid4()}',
        'user': 'USER#Setsuna',
        'title': 'Fusion énergétique activée',
        'body': 'Le mode final est enclenché, la bataille commence.',
        'image': f'https://{bucket}.s3.us-east-1.amazonaws.com/Setsuna/cf536095-f4b8-42ce-a6e9-b0be7b9e1566/a3df4756-399f-4517-bc1e-e387c1352df6trans+AM+00.jpg',
        'label': ['gundam', 'mecha', 'ultimate_form']
    }
]
