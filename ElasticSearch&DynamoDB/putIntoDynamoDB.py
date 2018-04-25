import boto3
from collections import Counter
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YelpData')

filelink = "s3://yelp-machine-learning-data-source/YelpList.txt"
rdd = sc.textFile(filelink).map(lambda x : x.split("\t"))

col = rdd.collect()

# putItem
def putIntoDB(x):
    buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code = x
    response = table.put_item(
        Item = {
            'buseness_id':buseness_id,
            'name': name,
            'address':address,
            'coordinates':coordinates,
            'number_of_reviews':number_of_reviews,
            'yelp_rating':yelp_rating,
            'categories':categories,
            'zip_code':zip_code
        }
    )
    return (x[0],response)

def ReportResponses(responseList):
    exceptions = []
    for buseness_id, response in responseList:
        http_code = response['ResponseMetadata']['HTTPStatusCode']
        if http_code<200 or http_code > 206:
            exceptions.append(buseness_id)
    total = len(responseList)
    successful = len(responseList)-len(exceptions)
    rate = "%d/%d put into Table. " %(successful,total) 
    if len(exceptions) > 0:
        log = "[Error]" + rate + "Failed buseness_id:" + ",".join(exceptions)
    else:
        log = "[Success]" + rate
    return log

responseList = []
for i,x in enumerate(col):
    if i % 100==0: print("[Process:]%d / %d" % (i,len(col)))
    r = putIntoDB(x)
    responseList.append(r)

ReportResponses(responseList)


