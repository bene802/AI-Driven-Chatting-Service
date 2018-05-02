#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:05:07 2018

@author: zhouyi
"""
FILE_1_PREDICTIONS = open("/Users/zhouyi/Desktop/FILE_1_PREDICTIONS.csv","r")
FILE_1 = open("/Users/zhouyi/Desktop/FILE_1.csv","r")
FILE_3 = open("/Users/zhouyi/Desktop/FILE_3.csv","w")
count = 0
for l1,l2 in zip(FILE_1,FILE_1_PREDICTIONS):
    buseness_id,category,yelp_rating,number_of_reviews = l1.strip("\n").split(",")
    buseness_id_,label,score = l2.strip("\n").split(",")
    if buseness_id != buseness_id:
        print("Not match",buseness_id,buseness_id_)
    if label == "1":
        count += 1
        line =(buseness_id,category,yelp_rating,number_of_reviews,score,label)
        print(*line, sep=",",end="\n",file=FILE_3)

print("line count in FILE_3: ", count)
FILE_1.close()
FILE_1_PREDICTIONS.close()
FILE_3.close()