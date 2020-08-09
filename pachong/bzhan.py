from tools.myrequests import _requests as request
from tools.myrequests import Headers as headers
import json
from pyquery import PyQuery
import time
import queue
import threading
import logging
from lxml import html


def get_followers_count(id):
    url = 'https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid={}'.format(id)

    response = request.get(url,headers=headers)
    info = json.loads(response.text)

    print(info['data']['follower'])


if __name__ == '__main__':
    # get_followers_count(321548603)
    url = 'https://b23.tv/8JESgv'
    response = request.get(url, headers=headers)
    print(response.text)