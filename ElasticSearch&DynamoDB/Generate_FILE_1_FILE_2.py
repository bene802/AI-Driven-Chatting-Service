import time
import requests

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
    buseness_id = item["id"]
    name = item["name"]
    address = ",".join(item["location"]["display_address"])
    coordinates = str(item["coordinates"]["latitude"]) + "," + str(item["coordinates"]["longitude"])
    number_of_reviews = item["review_count"]
    yelp_rating = item["rating"]
    categories = item["categories"][0]["title"]
    zip_code = item["location"]["zip_code"]
    
    return buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code

TotalScrape = set()

#searchSetting 
cityList = ['New York, New York', 'Los Angeles, California', 'Chicago, Illinois', 'Houston, Texas', 'Phoenix, Arizona', 'Philadelphia, Pennsylvania', 'San Antonio, Texas', 'San Diego, California', 'Dallas, Texas', 'San Jose, California', 'Austin, Texas', 'Jacksonville, Florida', 'San Francisco, California', 'Columbus, Ohio', 'Indianapolis, Indiana', 'Fort Worth, Texas', 'Charlotte, North Carolina', 'Seattle, Washington', 'Denver, Colorado', 'El Paso, Texas', 'Washington, D. C.', 'Boston, Massachusetts', 'Detroit, Michigan', 'Nashville, Tennessee', 'Memphis, Tennessee', 'Portland, Oregon', 'Oklahoma City, Oklahoma', 'Las Vegas, Nevada', 'Louisville, Kentucky', 'Baltimore, Maryland', 'Milwaukee, Wisconsin', 'Albuquerque, New Mexico', 'Tucson, Arizona', 'Fresno, California', 'Sacramento, California', 'Mesa, Arizona', 'Kansas City, Missouri', 'Atlanta, Georgia', 'Long Beach, California', 'Colorado Springs, Colorado', 'Raleigh, North Carolina', 'Miami, Florida', 'Virginia Beach, Virginia', 'Omaha, Nebraska', 'Oakland, California', 'Minneapolis, Minnesota', 'Tulsa, Oklahoma', 'Arlington, Texas', 'New Orleans, Louisiana', 'Wichita, Kansas']
cuisineList = ["Chinese","Japanese","Korean","American","Mexican","Italian","Indian"]

#search
for cuisine in cuisineList:
    for location in cityList:
        numberOfPeople = "2"
        diningTime = "20:00"
    
        # Yelp search setting
        api_key = "wCjcM1udNGY_x4YbCXHxWcJ3HirWGxGPem8yFp6EMBt81hAiz2oNBAPy6fF9FQNYrRsK_3ZCT_FJMDBThXkgq5MnEpj1dNrbU8606OkwCCbhHX7-gVZ8EpGY6ru-WnYx"
        payload = makePayloadYelp(cuisine, location, diningTime, numberOfPeople)
        host_url = "https://api.yelp.com/v3/businesses/search"
                    
        # Search using Yelp API
        search_result = searchYelp(api_key, payload, host_url)
        businesses = search_result["businesses"]
        searchList = list(map(extractYelp, businesses))
        TotalScrape = TotalScrape | set(searchList)


TotalList = list(TotalScrape)
# Write it into YelpList.txt
# buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code

#Generate FILE_2
def LikeFilter(x):
    buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code = x
    if number_of_reviews > 300 and yelp_rating >= 4.5:
        return True
    else:
        return False
def DislikeFilter(x):
    buseness_id,name,address,coordinates,number_of_reviews,yelp_rating,categories,zip_code = x
    if number_of_reviews > 300 and yelp_rating <= 3.5:
        return True
    else:
        return False
def FormatMapper(line):
    buseness_id = line[0]
    category = line[-2]
    yelp_rating = line[5]
    number_of_reviews = line[4]
    return buseness_id,category,yelp_rating,number_of_reviews
    
like = list(filter(LikeFilter,TotalList))[:100]
dislike = list(filter(DislikeFilter,TotalList))[:100]
FILE_2_LIST = []
for line in like:
    buseness_id,category,yelp_rating,number_of_reviews = FormatMapper(line)
    item = (buseness_id,category,yelp_rating,number_of_reviews,1)
    FILE_2_LIST.append(item)
for line in dislike:
    buseness_id,category,yelp_rating,number_of_reviews = FormatMapper(line)
    item = (buseness_id,category,yelp_rating,number_of_reviews,0)
    FILE_2_LIST.append(item)
    
FILE_2 = open("/Users/zhouyi/Desktop/FILE_2.csv","w")
for line in FILE_2_LIST:
    print(*line,sep=",",end="\n",file=FILE_2)
FILE_2.close()

#Generate FILE_1
FILE2_SET = set(list(map(lambda x :x[0],FILE_2_LIST)))
FILE_1 = open("/Users/zhouyi/Desktop/FILE_1.csv","w")
for line in TotalList:
    buseness_id,category,yelp_rating,number_of_reviews = FormatMapper(line)
    if buseness_id not in FILE2_SET:
        print(buseness_id,category,yelp_rating,number_of_reviews,sep=",",end="\n",file=FILE_1)
FILE_1.close()
        
    
    


