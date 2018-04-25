
# Create ES index predictions 
# Create ES type Prediction uder ES index predictions 
# (buseness_id,category,yelp_rating,number_of_reviews,score,label)
curl -X PUT "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions" -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 3, 
            "number_of_replicas" : 2 
        }
    },
    "mappings" : {
    	"Prediction" :{
		    "properties": { 
		        "buseness_id": { "type": "text" }, 
		        "category": { "type": "text" }, 
		        "yelp_rating": {"type":"float"},
		        "number_of_reviews": { "type": "integer" },
		        "score": {"type":"float"},
		        "label": {"type":"integer"}
		    }
		}
    }
}
'
# {"acknowledged":true,"shards_acknowledged":true,"index":"predictions"}% 

# -------------------------------------------------------------------------------------------------------------------------------------------------------- 



# check index & type
curl -X GET 'https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/_mapping?pretty=true'

# delete index
curl -X DELETE "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions"


# see the data entry
curl -X GET "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions/Prediction/1?pretty=true"

# search exact words
curl -X GET "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions/Prediction/_search" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match": {
            "category": "American (New)",
        }
    }
}
'

curl -X GET "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions/Prediction/_search" -H 'Content-Type: application/json' -d'
{
    "query": {
        "prefix": {
            "category": "American"
        }
    }
}
'


# put bulk
curl -XPOST "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/_bulk" -H 'Content-Type: application/json' -d '
{ "create": { "_index": "predictions", "_type":   "Prediction", "_id": "2" } }
{ "buseness_id":"72PQGMhrEcIuWH-S44TprA","category":"Asian Fusion","yelp_rating":4.0, "number_of_reviews": 1381,"score":"5.93E-01", "label":1}
{ "create": { "_index": "predictions", "_type":   "Prediction", "_id": "3" } }
{ "buseness_id":"0Jg0XmblNFayUIKbhfqTFA","category":"Japanese","yelp_rating":4.5, "number_of_reviews": 57,"score":"9.99E-0", "label":1}
'

curl -XPOST "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/_bulk" -H 'Content-Type: application/json' --data-binary  @./FILE_3.json


#search all records
curl -X GET "https://search-predictions-yelp-wdtlnynq7zxm6cn4tsmrqfayjm.us-east-1.es.amazonaws.com/predictions/Prediction/_search" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match_all" : {}
    }
}'
