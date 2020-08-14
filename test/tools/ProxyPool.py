# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

from tools.RedisQueue import RedisSet
from tools.e import TooManyRequest
import requests
import time
import logging
import ipdb

logging.basicConfig(level=logging.INFO)
zset = RedisSet('ips')
API = 'http://api.ip.data5u.com/dynamic/get.html?order=3021e9f5f605d61513bccd9a61b805a9&ttl=1&json=1&sep=3'

def getIP():
    """Get a proxy from API.

    :return: ip_port, ttl
    """
    resp = requests.get(API)

    if resp.status_code == 429:
        time.sleep(1)
        logging.warning('[429]too many requests')
        raise TooManyRequest

    elif resp.status_code == 200:
        text = resp.json()
        if text['success']:
            data = text['data'][0]
        else:
            logging.warning('[200]too frequent')
            time.sleep(1)
            raise TooManyRequest
    else:
        time.sleep(1)
        logging.error('Other Status Code: {}'.format(resp.status_code))
        raise Exception

    ip_port = '{}:{}'.format(data['ip'], data['port'])
    ttl = data['ttl'] / 1000 # data['ttl'] is ms
    return ip_port, ttl

def put():
    """Put the ip_port into Redis."""
    # ipdb.set_trace()
    ip_port, ttl = getIP()
    zset.add(ip_port, ttl)
    logging.info('[PUT INTO REDIS] %s' % ip_port)



def set_proxy():
    """Get one ip_port from Redis.

    :return: Formatted ip_port.
    """
    btext = zset.get()
    if btext:
        ip_port = btext.decode('utf-8')
        proxies = {
            'http': 'http://{}'.format(ip_port),
            'https': 'https://{}'.format(ip_port)}
        return proxies, ip_port

    else:
        return None, None


def rem_proxy(ip_port):
    """Remove unusable ip_port from Redis."""
    zset.rem(ip_port)
    logging.info('[REMOVE FROM REDIS] %s' % ip_port)


def main():
    """Loop to get ip and put it into Reids"""
    while True:
        try:
            put()
            time.sleep(4)
        except TooManyRequest:
            time.sleep(5)
        except Exception as e:
            logging.error('Unexpected Error!!!', e)



if __name__ == '__main__':
    main()