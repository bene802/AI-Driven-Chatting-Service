import boto3
import json

def lambda_handler(event, context):
  
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName="restaurant_sqs")
    queue.send_message(MessageBody=json.dumps(event))
    
    response = {"dialogAction": {
                            "type": "Close",
                            "fulfillmentState": "Fulfilled",
                            "message": {
                              "contentType": "PlainText",
                              "content": "You are all set."
                            }
                    }
        
                }
    return response