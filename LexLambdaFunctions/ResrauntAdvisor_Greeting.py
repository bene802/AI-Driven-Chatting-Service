def lambda_handler(event, context):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "Greetings! What can I do for you?"
                },
           
        }
    }
    return response