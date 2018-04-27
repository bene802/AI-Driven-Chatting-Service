import boto3
import json
import time
from botocore.vendored import requests
from botocore.exceptions import ClientError

def searchElastic(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "prefix": {
                    "category": term
            }
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.get(uri,headers=headers, data=query)
    results = json.loads(response.text)
    return results

def searchDynomoDB(table,buseness_id):
    response = table.get_item(
        Key={
        'buseness_id': buseness_id,
        }
    )
    return response
    
def extractDynamo(item):
    info = item["Item"]
    buseness_id = info["buseness_id"]
    name = info["name"]
    address = info["address"]
    coordinates = info["coordinates"]
    number_of_reviews = info["number_of_reviews"]
    yelp_rating = info["yelp_rating"]
    categories = info["categories"]
    zip_code = info["zip_code"]
    return buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code

def itemize(item):
    buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code = item
    return '''<h2>Name: {0} </h2>
              <p> Address: {1} </p> 
              <p> Rating: {2} </p> 
              <p> Number of reviews: {3} </p>
              <p> Category: {4} </p> '''.format(name,address,yelp_rating,number_of_reviews,categories)

def generateBodyHtml(searchList):
    content = "\r\n".join(list(map(itemize, searchList)))
    BODY_HTML = '''<html> 
    <head></head> 
    <body>
      <h1>Restraurants Recommended based on current query!</h3> 
      <hr>
      {0}
    </body>
    </html>
    '''.format(content)
    return BODY_HTML

def sendListToEmail(yelplist, email):
    searchList = yelplist
    SENDER = "RestraurantAdvisor <yz4029@nyu.edu>"
    RECIPIENT = email
    AWS_REGION = "us-east-1"
    SUBJECT = "Restraurants Recommendations based on your current query is now available!"
    CHARSET = "UTF-8"   
     # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (json.dumps(searchList))
    # The HTML body of the email.
    BODY_HTML = generateBodyHtml(searchList)
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
    
    
    
def lambda_handler(event, context):
    sqs = boto3.resource("sqs")
    sns = boto3.client('sns')
    queue = sqs.get_queue_by_name(QueueName="restaurant_sqs")
    res = []
    count = 0
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        
        count += 1
        # Extract info from Lex
        d = json.loads(message.body)
        currentIntent = d["currentIntent"]
        cuisine = currentIntent["slots"]["cuisine"]
        location = currentIntent["slots"]["location"]
        numberOfPeople = currentIntent["slots"]["numberOfPeople"]
        diningTime = currentIntent["slots"]["diningTime"]
        email = currentIntent["slots"]["email"]
        
        # get businese ids from  Elastic Search
        uri = "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions/Prediction/_search"
        term = cuisine.lower()
        results = searchElastic(uri,term)
        businese_ids = list(map(lambda x:x["_source"]["buseness_id"] ,results['hits']['hits']))
    
        # search DynamoDB
        dy_reponseList = []
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('YelpData')
        for businese_id in businese_ids:
            dy_response = searchDynomoDB(table, businese_id)
            dy_reponseList.append(dy_response)
        searchList = list(map(extractDynamo,dy_reponseList))
        
        # send to email
        RECIPIENT = email
        sendListToEmail(searchList, RECIPIENT)
        res.append([RECIPIENT, searchList])
        
    return (res,count)
