# -***coding=utf-8***-
# zaj_models.py，存放数据库操作
import pymysql
from tool.db import connect,find,findall

users_db = connect().users

def isUserExist(username):
    """判断用户名是否存在"""
    res = list(find(users_db,{'username': username}))
    if res == []:
        res = 0
    # res返回的是sql语句查询结果的个数；
    #  如果为0， 没有查到。
    if res == 0:
        return  False
    else:
        return  True

def isPasswdOk(username, passwd):
    res = list(find(users_db,{'username': username}))
    try:
        if res[0]['passwd'] == passwd:
            res = 1
        else:
            res = 0
    except:
        res = 0
    if res == 0:
        return False
    else:
        return True

def addUser(username, passwd):
    """用户注册时， 添加信息到数据库中"""
    try:
        res = {
            'username':username,
            'passwd':passwd
        }
        users_db.insert(res)
    except Exception as e:
        return e



if __name__ == "__main__":
    # addUser('root', 'root')
    print(isUserExist('admin'))
    print(isPasswdOk('admin', '123456789'))
