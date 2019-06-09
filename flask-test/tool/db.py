# -***coding=utf-8***-
from pymongo import MongoClient
import pymysql



#连接
def connect():
    client = MongoClient('47.106.37.156', 27017)
    db = client.main
    return db

def connect_user():
    client = MongoClient('47.106.37.156', 27017)
    db = client.users
    return db

def connect_recommend():
    client = MongoClient('47.106.37.156', 27017)
    db = client.recommend
    return db

def connect_history():
    client = MongoClient('47.106.37.156', 27017)
    db = client.history
    return db

#查询
def inquire(user,category,value):
    return user.find({category:value})


def findall(collection):
    return collection.find().batch_size(500)

def find(collection,some):
    return collection.find(some)




def sql_connect():
    db = pymysql.connect(host='127.0.0.1', user='root', password='xu199704', db='test', port=3306, charset='utf8')
    return db

def sql_insert(db,sql):
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

