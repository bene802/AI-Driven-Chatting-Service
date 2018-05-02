#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 20:18:05 2018

@author: zhouyi
"""

FILE_3 = open("/Users/zhouyi/Desktop/FILE_3.csv","r")
FILE_3_JSON = open("/Users/zhouyi/Desktop/FILE_3.json","w")
count = 0
for i,line in enumerate(FILE_3):
    count += 1
    create_line = '{ "create": { "_index": "predictions", "_type":   "Prediction", "_id": "%d" } }' % i
    buseness_id,category,yelp_rating,number_of_reviews,score,label = line.strip("\n").split(",")
    score = eval(score)
    yelp_rating = eval(yelp_rating)
    number_of_reviews = eval(number_of_reviews)
    category = category.lower()
    label = eval(label)
    data_line = '{ "buseness_id":"%s", "category": "%s","yelp_rating": %.1f, "number_of_reviews": %d, "score": %f, "label": %d}' % (buseness_id,category,yelp_rating,number_of_reviews,score,label)
    print(create_line,file=FILE_3_JSON,end="\n")
    print(data_line,file=FILE_3_JSON,end="\n")

FILE_3.close()
FILE_3_JSON.close()
print("documents count: ",count)