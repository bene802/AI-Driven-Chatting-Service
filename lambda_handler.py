import random
import uuid
import boto3
from datetime import datetime
def lambda_handler(event, context):
    if 'messages' in event:
        messages = event['messages']
    else:
        messages = []
    responds = []
    for message in messages:
        ##############request#######################
        type = message["type"]
        unstructured = message["unstructured"]
        id = unstructured["id"]
        text = unstructured["text"]
        timestamp = unstructured["timestamp"]
        ##############respond#######################
        respond = dict()
        respond['id'] = str(uuid.uuid4())
        respond['text'] = respoendTo(text)
        respond['timestamp'] = datetime.now().isoformat(timespec='seconds')
        responds.append(respond)
    return {"messages":responds}

def respoendTo(s):
    client = boto3.client('lex-runtime', region_name='us-east-1')
    response = client.post_text(
        botName = 'RestraurantAdvisor',
        botAlias = 'emailVersion',
        userId = 'LexChat',
        inputText = s
        )
    return response["message"]
