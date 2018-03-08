import random
import uuid
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
    if "Hello" in s:
        return "Hi there, how can I help?"
    elif "Hi" in s:
        return "What a nice day!"
    elif s == "?":
        return "What's your problem, I am here to help!"
    elif "?" in s:
        return "I see your problem. But I don't know either. I will send it to one of my manager."
    elif "name" in s:
        return "My name is Robot! Nice to meet you!"
    randomlist = [
        "Emmm...",
        "I don't quite understand",
        "Well, that sounds good.",
        "OMG, I feel sorry to hear that.",
        "I like your idea!",
        "What a pity",
        "I feel honored to talk to you.",
        "There must be something wrong",
        "I am glad to hear that"
    ]
    l = len(randomlist)
    pick = random.randint(0,l-1)
    return randomlist[pick]