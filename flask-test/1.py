# -***coding=utf-8***-
from tool.db import connect,find,findall,connect_user
import requests

def fun(user):
    user_db = connect_user()[user]
    keys = findall(user_db)[0]['keys']
    print(keys)
    count = 0
    for i in keys.keys():
        count += 1
    print(count)
    # user_db.update_one({'keys':keys}, {"$set":{'keys':{'a':2,'b':1}}})


fun('root')
