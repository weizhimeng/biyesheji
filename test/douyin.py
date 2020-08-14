from tools.myrequests import _requests as request
from tools.myrequests import Headers as headers
import json
from pyquery import PyQuery
import time
import queue
import threading
import logging
from lxml import html


android_headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
    }

def get_data(itemid):
    url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&dytk='.format(itemid)
    response = request.get(url, headers=android_headers)
    info = json.loads(response.text)
    comment_count = info['item_list'][0]['statistics']['comment_count']
    digg_count = info['item_list'][0]['statistics']['digg_count']
    data = {
        'comment_count': comment_count,
        'digg_count': digg_count,
    }
    print(data)
    return data


def get_followers_count(id):
    url = 'https://www.iesdouyin.com/web/api/v2/user/info/?{}'.format(id)
    response = request.get(url, headers=android_headers)
    info = json.loads(response.text)
    followers_count = info['user_info']['follower_count']
    print(followers_count)
    return followers_count

# def get_id(url,num,symbol):
#     req_url = 'https://duanwangzhihuanyuan.51240.com/web_system/51240_com_www/system/file/duanwangzhihuanyuan/get/?ajaxtimestamp=1597288171342'
#     data = {
#         'turl':url
#     }
#     response = request.post(req_url,data=data,headers=headers)
#     real_url = html.etree.HTML(response.text).xpath('//a//@href')[0]
#     itemid = real_url.split(symbol)[num]
#     return itemid

def get_id(url,num,symbol):
    response = request.get(url, headers=android_headers)
    real_url = response.url
    itemid = real_url.split(symbol)[num]
    print(itemid)
    return itemid

itemid = get_id('https://v.douyin.com/JjGBBjc/',5,'/')
id = get_id('https://v.douyin.com/JjG2EQ2/',1,'&')
get_followers_count(id)
get_data(itemid)

# response_xpath = ''.join(html.etree.HTML(response.text).xpath('//head//link[@rel="canonical"]//@href'))
# id = response_xpath.split('/')[4].replace('av', '')

# url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/hot/search/video/list/?hotword=%E6%AD%A6%E6%B1%89%E8%A2%AB%E6%89%93%E5%9F%8E%E7%AE%A1%E6%9C%AC%E4%BA%BA%E5%9B%9E%E5%BA%94&offset=0&count=50&source=trending_page&is_ad=0&item_id_list&is_trending=0&city_code&os_api=23&device_type=MI%205s&ssmix=a&manifest_version_code=100401&dpi=240&uuid=008796756562420&app_name=aweme&oaid=02af6cfa-4ce9-4d25-9856-3efc22aa4a1e&version_name=10.4.0&ts=1597391894&app_type=normal&ac=wifi&update_version_code=10409900&channel=tengxun_new&_rticket=1597391895169&device_platform=android&iid=1002356853444478&version_code=100400&cdid=afc936be-b8a6-40f5-b386-2318a954b4df&openudid=334d18eeba5e30d0&device_id=71311029000&resolution=720*1280&os_version=6.0.1&language=zh&device_brand=Xiaomi&aid=1128'