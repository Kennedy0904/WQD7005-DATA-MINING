# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:54:40 2020

@author: FORGE-15 I7
"""
from impala.dbapi import connect
conn = connect(host='192.168.0.28', 
               port=10000,
               user='Kennedy',
               database='default', 
               auth_mechanism="PLAIN")
cur = conn.cursor()
# createSQL = "CREATE TABLE if not exists news (NewsID string, PublishedDate string, PublishedTime string, Category string, Headline string, URL string) \
#     row format delimited fields terminated by ',' tblproperties ('skip.header.line.count'='1')"  
# cur.execute(createSQL)

# insertSQL = "load data inpath 'file:////D:/dataset.csv' into table news"
# cur.execute(insertSQL)

showSQL = "select* from news"
cur.execute(showSQL)
print(cur.fetchall())
    