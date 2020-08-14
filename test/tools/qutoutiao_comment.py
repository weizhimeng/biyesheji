# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')


from requests.exceptions import Timeout, ConnectTimeout, ReadTimeout, HTTPError, ConnectionError
from tools.myrequests import _requests as requests
from tools.e import NewPageElement
from tools.image import get_img_size
from tools.ProxyPool import set_proxy, rem_proxy
from tools.alert_email import send_email
import json
import logging
import time
from lxml import etree
import re
from tools.RedisQueue import RedisQueue



queue = RedisQueue('qutoutiao')
key = ['趣头条','头条']
def judge(content,key):
    for key in key:
        if key in content:
            return True
        else:
            return False

def rez(cent,text):
    cent = re.compile(cent)
    return re.findall(cent,text)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S', level=logging.INFO)

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
            'source': '趣头条',
            'data': [
                {
                    'url': self.url,  # 资讯链接
                    'title': data['title'],  # 资讯标题
                }
            ]
        }


    def prejudge(self):
        """Pre-processing before parse page

        :return: None
        """
        reput = False
        proxies, self.ip = set_proxy()
        try:
            self.response = requests.get(self.url, proxies=proxies, timeout=15)
            self.response.raise_for_status()
            self.response.encoding = 'utf-8'
            self.response.xpath = etree.HTML(self.response.text).xpath
        except (Timeout, ConnectTimeout, ReadTimeout) as e:
            self.response = None
            logging.error('请求超时:' + str(e))
            rem_proxy(self.ip)
        except ConnectionError as e:
            reput = True
            logging.error('网络中断连接错误:' + str(e))
            rem_proxy(self.ip)
        except HTTPError as e:
            self.response = None
            logging.error('Http错误:' + str(e))
            rem_proxy(self.ip)

        return reput



    def parse(self):
        """Parse  page detail
        post给后端接口
        :return: None
        """
        reput = self.prejudge()
        if reput: return reput
        if self.response:
            is_post = True
            try:
                self.get_comment()
                print(self.demo_data)
            except Exception as e:
                logging.error(e)
        else:
            return None
        if is_post:
            # resp = requests.post('http://meiri-import.newtvmall.com/api/import/news', json=self.demo_data)
            print(self.demo_data)
            # resp = requests.post('http://192.168.99.30:8081/api/import/news', json=self.demo_data)
            # if resp.json()['success']:
            #     url = self.demo_data['data'][0]['url']
            #     title = self.demo_data['data'][0]['title']
            #     logging.info('POST SUCCESS.IP:%s Url: %s, Title: %s' % (self.ip, url, title))
            # else:
            #     logging.error('POST FAILED.')
            #     logging.error(resp.text)
        else:
            logging.error("Data lost.Don't send to backend.Error URL: %s" % self.url)


    def get_comment(self):
        comments = []
        proxies, self.ip = set_proxy()
        page = 1
        count = 0
        while True:
            url = 'https://api.1sapp.com/comment/?content_id={}&page={}'.format(self.id,page)
            response = requests.get(url, proxies=proxies, timeout=15)
            ob_json = json.loads(response.text)
            for data in ob_json['data']:
                comment_id = data['comment_id']
                comment_text = data['comment']
                reply_count = data['reply_number']
                create_time = str(data['create_time'])
                create_time = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
                create_time = int(time.mktime(create_time))
                digg_count = data['like_num']
                user_name = data['nickname']
                avatar = data['avatar']
                info = {
                    'originId': comment_id,
                    'content': comment_text,
                    'reply_count': reply_count,
                    'publishTime': create_time,
                    'likeNum': digg_count,
                    'username': user_name,
                    'avatar': avatar,
                    # 'replies': [],
                }
                # replies = []
                # for reply in data['reply_list']:
                #     comment_id = reply['comment_id']
                #     comment = reply['comment']
                #     create_time = str(reply['create_time'])
                #     create_time = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
                #     create_time = int(time.mktime(create_time))
                #     nickname = reply['nickname']
                #     like_num = reply['like_num']
                #     avatar = reply['avatar']
                #     reply_info = {
                #         'originId': comment_id,
                #         'content': comment,
                #         'publishTime': create_time,
                #         'likeNum': like_num,
                #         'username': nickname,
                #         'avatar': avatar,
                #     }
                #     replies.append(reply_info)
                # info['replies'] = replies
                comments.append(info)
            count += 1
            if count >= 5:
                break
            page += 1
        self.result['comments'] = comments




