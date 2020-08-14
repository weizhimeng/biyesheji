# -*- coding: utf-8 -*-
import json
import requests
from pymongo import MongoClient

PROXY_URL = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'

def loginDB():
    """
    login to mongodb
    :return: proxy colleciton
    """
    client = MongoClient('127.0.0.1', 27017)
    db = client.mongo
    proxy = db['proxy']
    return proxy

PROXY = loginDB()

def getProxy():
    """
    提取较好的代理
    数据格式
        {
            "port": 33186, "export_address": ["159.224.44.188"],
            "host": "159.224.44.188", "country": "UA", "response_time": 1.2,
            "anonymity": "high_anonymous", "type": "http", "from": "freeproxylist"
        }
    """
    response = requests.get(PROXY_URL)

    # 将字符串格式的数据以[{},{},{}...]形式存储
    json_data = [json.loads(item) for item in response.text.split('\n') if item]

    # 清洗json_data得到高匿代理
    plist = [item for item in json_data if item['anonymity']=='high_anonymous' and item['country']=='CN']

    # 将export_address改为_id, 更新数据为host:port形式
    for item in plist:
        _id = '{host}:{port}'.format(host=item['host'], port=item['port'])
        item.setdefault('_id', _id)     # 保证唯一性
        item.setdefault('score', 100)   # 刚入库分数设置为100
        del item['export_address']
        del item['from']
    return plist

def proxyInMongo(plist):
    """存储代理到mongodb中"""
    count = 0
    # 连接mongodb.local.proxy

    for post in plist:
        if not PROXY.find_one({'_id': post['_id']}):
            result = PROXY.insert_one(post)
            count += 1
            print('One post:{}'.format(result.inserted_id))
        else:
            print('The {host}:{port} has existed'.format(host=post['host'], port=post['port']))

    all = PROXY.find().count()
    print('{0} additional agents,there are currently {1} agents'.format(count, all))




def getOneProxy():
    """
    get a proxy form mongodb
    :return: one proxy ip_port
    """
    pipeline = [{'$match': {'score': 100}}, {'$sample': {'size': 1}}]
    cursor = PROXY.aggregate(pipeline)
    result = list(cursor)[0]
    return result['_id']

def decrease(_id):
    """
    when one ip can't use or can't use,score minus 5
    :param _id: proxy ip_port
    :return: None
    """
    PROXY.find_one_and_update({'_id': _id}, {'$inc': {'score': -5}})

def set_status(_id):
    """
    when one
    :param _id: proxy ipp_port
    :return: None
    """
    PROXY.find_one_and_update({'_id': _id}, {'$set': {'score': 404}})


def main():
    """主程序"""
    plist = getProxy()
    proxyInMongo(plist)


if __name__ == '__main__':
    main()