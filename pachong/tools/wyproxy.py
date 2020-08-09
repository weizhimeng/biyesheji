# -*- coding: utf-8 -*-
# 无忧代理
# API接口限制：
    # 第一点，API接口规定1秒钟最多请求10次（两次请求间隔100毫秒以上，否则HTTP返回状态码为429），
    # 并不是每次请求都会返回新的IP，接口每隔5秒会返回新IP。所以你在5秒内重复调用接口，返回的都是一样的IP。

    # 第二点，API接口最多允许5个不同的外网IP调用，如果超过5个调用IP，那么接口会返回：
    # 每个订单号最多支持5个不同IP调用，10分钟后自动解除本限制！如果出现该提示，请检查是否存在以下原因：
    # 1) 设置了代理IP，然后用代理IP请求接口
    # 2) 出口IP是动态变化的，是否使用了拨号服务器
    # 3) 是否把单号泄露给了他人

    # 如果单号泄露，可以到用户中心-IP白名单中启用白名单功能并添加自己的IP，启用后只有白名单IP才能调用接口。
import time
import requests
import logging
from random import random
# 返回数据格式为JSON，优先返回可用时间长的IP
# URL = 'http://api.ip.data5u.com/dynamic/get.html?order=3021e9f5f605d61513bccd9a61b805a9&ttl=1&json=1&random=true&sep=3'
# 返回数据格式为JSON，优先返回速度快的IP
URL = 'http://api.ip.data5u.com/dynamic/get.html?order=3021e9f5f605d61513bccd9a61b805a9&ttl=1&json=1&sep=3'

logging.basicConfig(level=logging.INFO)
def get_proxy(url=URL):
    """get one ip from API"""
    resp = requests.get(url)

    if resp.status_code == 429:
        time.sleep(3)
        logging.warning('[429]too many requests')
        raise Exception

    elif resp.status_code == 200:
        text = resp.json()
        if text['success']:
            data = text['data'][0]
        else:
            logging.warning('[200]too frequent')
            time.sleep(1)
            raise Exception
    else:
        time.sleep(3)
        logging.error('Other Status Code: {}'.format(resp.status_code))
        raise Exception
    ip = data['ip']
    port = str(data['port'])
    ip_port = ''.join([ip, ':', port])
    return ip_port

def set_proxy(url=URL):
    """Reset Proxy IP

    :return: None
    """
    # 优先返回速度快的IP
    time.sleep(random() * 5)
    while True:
        try:
            ip_port = get_proxy(url)
            break
        except:
            logging.error('获取IP出错')
            time.sleep(random() * 5)

    proxies = {
        'http': 'http://{}'.format(ip_port),
        'https': 'https://{}'.format(ip_port)
    }
    return proxies, ip_port

