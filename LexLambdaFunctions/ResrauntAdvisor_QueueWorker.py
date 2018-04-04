import boto3
import json
import time
from botocore.vendored import requests
from botocore.exceptions import ClientError

def todayUnixTime(diningTime):
    """
    :diningTime: str, eg "19:00"
    :return:  int, a unix timestamp
    """
    try:
        hour,minu = diningTime.split(":")
        now = time.localtime(time.time())
        fmt = '%Y-%m-%d %H:%M:%S'
        Date = time.strftime(fmt,time.localtime(time.time()))
        searchTime = Date[:11] + "%s:%s:00" % (hour, minu)
        searchTuple = time.strptime(searchTime, fmt)
        unixTimeStamp = int(time.mktime(searchTuple))
    except:
        now = time.time()
        unixTimeStamp = int(now)
    return unixTimeStamp

def makePayloadYelp(cuisine, location, diningTime, numberOfPeople=2):
    """
    Note: numberOfPeople ignored for yelp search
    """
    payload = {'term': cuisine, 
           'location': location,
           "open_at":todayUnixTime(diningTime),
           }
    return payload

def searchYelp(api_key, payload, host_url):
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    r = requests.get(host_url, headers=headers, params=payload)
    search_result = r.json()
    return search_result

def extractYelp(item):
    name = item["name"]
    yelp_rating = item["rating"]
    categories = item["categories"][0]["title"]
    address = ",".join(item["location"]["display_address"])
    image_url = item["image_url"]
    return name,yelp_rating,categories,address,image_url

def itemize(item):
    return '''<h2> {0} </h2>
              <p> Rating: {1} </p> 
              <p> Style: {2} </p> 
              <p> Address: {3} 
              </p><img src="{4}" width="500" height="300" >'''.format(item[0],item[1],item[2],item[3],item[4])

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
        
        # Yelp search setting
        api_key = "wCjcM1udNGY_x4YbCXHxWcJ3HirWGxGPem8yFp6EMBt81hAiz2oNBAPy6fF9FQNYrRsK_3ZCT_FJMDBThXkgq5MnEpj1dNrbU8606OkwCCbhHX7-gVZ8EpGY6ru-WnYx"
        payload = makePayloadYelp(cuisine, location, diningTime, numberOfPeople)
        host_url = "https://api.yelp.com/v3/businesses/search"
            
        # Search using Yelp API
        search_result = searchYelp(api_key, payload, host_url)
        businesses = search_result["businesses"]
        searchList = list(map(extractYelp, businesses))
        message.delete()
        
        
        #send to email
        RECIPIENT = email
        sendListToEmail(searchList, RECIPIENT)
        res.append([RECIPIENT, searchList])
        
    
    return (res,count)