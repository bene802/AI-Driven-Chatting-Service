def lambda_handler(event, context):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "PlainText",
              "content": "You are welcome. It's my honor to assist you."
                },
           
        }
    }
    return response
