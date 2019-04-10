# -*- coding: utf-8 -*-
from pymongo import MongoClient
def connect():
    client = MongoClient('47.106.37.156', 27017)
    db = client.test
    return db

def findall(collection):
    return collection.find().batch_size(500)

news_db = connect().news_keys
news = findall(news_db)
yule = connect().yule
keji = connect().keji
dongman = connect().dongman
tiyu = connect().tiyu
guoji = connect().guoji
lishi = connect().lishi
count = 0
for new in news:
    cat = new['category']
    if cat in ['娱乐']:
        yule.insert(new)
    if cat in ['科技']:
        keji.insert(new)
    if cat in ['动漫']:
        dongman.insert(new)
    if cat in ['体育']:
        tiyu.insert(new)
    if cat in ['国际', '军事']:
        guoji.insert(new)
    if cat in ['历史']:
        lishi.insert(new)
    count += 1
    print(count)

