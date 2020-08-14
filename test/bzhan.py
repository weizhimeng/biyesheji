from tools.myrequests import _requests as request
from tools.myrequests import Headers as headers
import json
from pyquery import PyQuery
import time
import queue
import threading
import logging
from lxml import html


def get_id(url):
    response = request.get(url, headers=headers)
    response_xpath = ''.join(html.etree.HTML(response.text).xpath('//head//link[@rel="canonical"]//@href'))
    id = response_xpath.split('/')[4].replace('av', '')
    print(id)
    return id

def get_id_article(url):
    id = url.split('/')[4].replace('cv', '')
    print(id)
    return id

def get_followers_count(id):
    url = 'https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid={}'.format(id)

    response = request.get(url,headers=headers)
    info = json.loads(response.text)

    print(info['data']['follower'])

def get_data(id):
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(id)
    response = request.get(url, headers=headers)
    info = json.loads(response.text)
    coin = info['data']['coin']
    like = info['data']['like']
    view = info['data']['view']
    share = info['data']['share']
    favorite = info['data']['favorite'] #收藏
    data = {
        'coin': coin,
        'like': like,
        'view': view,
        'share': share,
        'favorite': favorite
    }
    print(data)

def get_data_article(id):
    url = 'https://api.bilibili.com/x/article/viewinfo?id={}&mobi_app=h5&from=homepage_0&jsonp=jsonp'.format(id)
    response = request.get(url, headers=headers)
    info = json.loads(response.text)
    coin = info['data']['stats']['coin']
    like = info['data']['stats']['like']
    view = info['data']['stats']['view']
    comment = info['data']['stats']['reply']
    share = info['data']['stats']['share']
    favorite = info['data']['stats']['favorite'] #收藏
    data = {
        'coin': coin,
        'like': like,
        'view': view,
        'comment': comment,
        'share': share,
        'favorite': favorite
    }
    print(data)

if __name__ == '__main__':
    get_followers_count(321548603)
    url = 'https://b23.tv/8JESgv'
    id = get_id(url)
    get_data(id)
    url = 'https://www.bilibili.com/read/cv6878041/?from=homepage_0&spm_id_from=333.851.b_62696c695f7265706f72745f72656164.22'
    id = get_id_article(url)
    get_data_article(id)
