# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '')

from requests.exceptions import Timeout, ConnectTimeout, ReadTimeout, HTTPError, ConnectionError
from tools.myrequests import _requests as requests
from tools.ProxyPool import set_proxy, rem_proxy
from tools.e import NewPageElement
from urllib.parse import urlparse
import re
import html
from lxml import etree
import logging
import json
from multiprocessing.dummy import Pool
from tools.alert_email import send_email

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.INFO)

key = ['今日头条','头条','JRTT','jrtt','张一鸣','一鸣','字节跳动','头条新闻','头条号','陈林','内涵段子','头条寻人']
def judge(content,key):
    for key in key:
        if key in content:
            return True
        else:
            return False
# INVALID_DOMAINS = ['m2.people.cn', 'm.gmw.cn', '3w.huanqiu.com', 'm.toutiao.com']


CATEGORY_MAP = {
    'news_entertainment' :  '娱乐',
    'news_finance' :        '财经',
    'news_tech' :           '科技',
    'news_sports' :         '体育',
    'news_car' :            '汽车',
    'news_travel' :         '旅行',
    'news_history' :        '历史',
    'news_game' :           '游戏',
    'news_baby' :           '育儿',
    'news_world' :          '国际',
    'news_health' :         '健康',
    'news_house' :          '房产',
    'news_agriculture':     '三农',
    'news_culture':         '文化',
    '宠物':                  '宠物'

}

class Comment():

    def __init__(self, data):
        self.is_post = True
        self.newsId = data['newsId']
        self.url = data['url']
        self.id = self.url.strip().split('/')[-2]
        self.comment_url = 'https://ic.snssdk.com/article/v4/tab_comments/?group_id={}&item_id={}&count=100'.format(self.id,self.id)
        self.result = {
            'newsId': self.newsId,
            "sourceId": data['sourceId'],
            'comments': []
        }
        self.demo_data = {
            'source': '今日头条',
            'data': [
                {
                    'url': self.url,  # 资讯链接
                    'title': data['title'],  # 资讯标题
                }
            ]
        }


    def prejudge(self):
        """Pre-processing before parse page
        判断爬取是否需要重新放回redis
        :return: None
        """
        reput = False
        proxies, self.ip = set_proxy()
        try:
            self.response = requests.get(self.comment_url, proxies=proxies, timeout=9)
            if json.loads(self.response.text)['message'] != 'success':
            # netloc1 = urlparse(self.response.url).netloc
            # netloc2 = urlparse(self.url).netloc
            # if (netloc1 or netloc2) != 'www.toutiao.com' :
                logging.warning('invalid page:{}'.format(self.url))
                self.response = None
        except (Timeout, ConnectTimeout, ReadTimeout) as e:
            self.response = None
            logging.info('请求超时:' + str(e))
            rem_proxy(self.ip)
        except ConnectionError as e:
            reput = True
            logging.info('网络中断连接错误:' + str(e))
            rem_proxy(self.ip)
        except HTTPError as e:
            self.response = None
            logging.info('Http错误:' + str(e))
            rem_proxy(self.ip)


        return reput



    def parse(self):
        """Parse  page detail
        post给后端接口
        :return: None
        """
        reput = self.prejudge()
        if reput: return reput
        try:
            if self.response:
                self.get_comment()
        except Exception as e:
            logging.error(e)
            self.is_post = False
            self.reput = True
            return self.reput
        if self.result['comments'] == []:
            self.is_post = False
        if self.is_post:
            resp = requests.post('http://qmtest.newtvmall.com/api/import/news/comment', json=self.result)
            print(self.result)
            # resp = requests.post('http://meiri-import.newtvmall.com/api/import/news', json=self.demo_data)
            if resp.json()['success']:
                url = self.demo_data['data'][0]['url']
                title = self.demo_data['data'][0]['title']
                logging.info('POST SUCCESS.IP:%s Url: %s, Title: %s' % (self.ip, url, title))
            else:
                logging.error('POST FAILED.')
                logging.error(resp.text)
        else:
            logging.error("Data lost.Don't send to backend.Error URL: %s" % self.url)


    def get_comment(self):
        comments = []
        proxies, self.ip = set_proxy()
        response = requests.get(self.comment_url, proxies=proxies, timeout=9).text
        ob_json = json.loads(response)
        count = 0
        for comment in ob_json['data']:
            comment = comment.get('comment')
            comment_text = comment.get('text')
            if judge(comment_text,key):
                continue
            reply_count = int(comment.get('reply_count'))
            create_time = int(comment.get('create_time'))
            dongtai_id = comment.get('id')
            try:
                digg_count = comment.get('digg_count')
            except:
                digg_count = 0
            user_name = comment.get('user_name')
            user_profile_image_url = comment.get('user_profile_image_url')
            info = {
                'originId':dongtai_id,
                'content': comment_text,
                'publishTime': create_time,
                'likeNum': digg_count,
                'username': user_name,
                'avatar': user_profile_image_url,
                # 'replies': [],
            }
            # if reply_count > 0:
            #     rep = []
            #     url = 'https://www.toutiao.com/api/comment/get_reply/?comment_id={}&offset=0&count=20'.format(dongtai_id)
            #     headers = {
            #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
            #
            #     response = requests.get(url,proxies=proxies,timeout=3,headers=headers).text
            #     ob_json = json.loads(response)
            #     for reply in ob_json['data']['data']:
            #         reply_text = reply.get('text')
            #         if judge(reply_text, key):
            #             continue
            #         reply_create_time = int(reply.get('create_time'))
            #         name = reply.get('user').get('name')
            #         avatar_url = reply.get('user').get('avatar_url')
            #         originId = reply.get('id')
            #         try:
            #             digg_count = reply.get('digg_count')
            #         except:
            #             digg_count = 0
            #         reply_info = {
            #             'originId':originId,
            #             'content': reply_text,
            #             'publishTime': reply_create_time,
            #             'likeNum': digg_count,
            #             'username': name,
            #             'avatar': avatar_url,
            #         }
            #         rep.append(reply_info)
            #     info['replies'] = rep
            comments.append(info)
            count += 1
            if count >= 5:
                break
        self.result['comments'] = comments




