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
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(id)

    response = request.get(url,headers=headers)
    info = json.loads(response.text)

    print(info['data']['userInfo']['followers_count'])

def get_data(id):
    url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}'.format(id)
    response = request.get(url, headers=headers)
    info = json.loads(response.text)
    forward = info['data']['total_number']

    url = 'https://m.weibo.cn/api/comments/show?id={}'.format(id)
    response = request.get(url, headers=headers)
    info = json.loads(response.text)
    comments = info['data']['total_number']

    url = 'https://m.weibo.cn/api/attitudes/show?id={}'.format(id)
    response = request.get(url, headers=headers)
    info = json.loads(response.text)
    attitudes = info['data']['total_number']

    data = {
        'forward':forward,
        'comments': comments,
        'attitudes': attitudes,
    }
    print(data)

if __name__ == '__main__':
    get_followers_count(3099016097)
    get_data(4532355803646445)