# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')


from requests.exceptions import Timeout, ConnectTimeout, ReadTimeout, HTTPError, ConnectionError
from tools.myrequests import _requests as requests
from tools.e import NewPageElement
from tools.image import get_img_size
from tools.ProxyPool import set_proxy, rem_proxy
from tools.ttkb_params import comment_headers_gen
from multiprocessing.dummy import Pool
import logging
import time
import json
import re

key = ['天天快报','快报','TTKB','ttkb','关心世界','更关心你','企鹅号','腾讯兴趣阅读平台']
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

NEWS_TYPE_MAP = {
    'kb_news_beauty':   '美女',
    'kb_news_sex':      '情感',
    'kb_news_laugh':    '搞笑',
    'kb_news_bagua':    '娱乐',
    'kb_news_mil':      '军事',
    'kb_photo_gif':     'GIF',
    'kb_news_erciyuan': '动漫',
    'kb_news_chaobao':  '时尚',
    'kb_news_astro':    '星座',
}

class Comment():

    def __init__(self, data):
        self.newsId = data['newsId']
        self.url = data['url']
        self.id = self.url.strip().split('/')[-1]
        self.result = {
            'newsId':self.newsId,
            "sourceId": data['sourceId'],
            'comments':[]
        }
        self.demo_data = {
            'source': '天天快报',
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
            url = 'http://kuaibao.qq.com/s/{}'.format(self.id)
            self.response = requests.get(url, proxies=proxies, timeout=15)
            self.response.raise_for_status()
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

        :return: None
        """
        reput = self.prejudge()
        if reput: return reput
        if self.response:
            is_post = self.get_comment()
            print(self.result)
        else:
            return None
        if is_post:
            resp = requests.post('http://meiri-import.newtvmall.com/api/import/news', json=self.demo_data)
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
        is_post = True
        comments = []
        try:
            url = 'http://kuaibao.qq.com/s/{}'.format(self.id)
            response = self.response.text
            cent = r'commentId = "(.*?)";'
            comment_id = ''.join(rez(cent, response))
            reply_ids = []
            reply_ids2 = []
            headers = comment_headers_gen()
            url = 'https://r.cnews.qq.com/getQQNewsComment?'
            num = 0
            try:
                reply_id = reply_ids[-1]
            except:
                reply_id = ''
            body = 'showType=orig&comment_id={}&url=https%3A%2F%2Fkuaibao.qq.com%2Fs%2FTWF2018122700268300%3Frefer%3Dkb_news%26titleFlag%3D2%26omgid%3D13c6b4e00a321df7bcde7d4d509d87eb&reply_id={}&sortType=hot'.format(
                comment_id, reply_id)
            resp = requests.post(url, headers=headers, data=body)
            resp.encoding = 'utf-8'
            resp = resp.text
            ob_json = json.loads(resp)
            for hot_comment in ob_json['comments']['hot']:
                rep = []
                count = 0
                comment_text = hot_comment[0]['reply_content']
                create_time = int(hot_comment[0]['pub_time'])
                try:
                    digg_count = hot_comment[0]['agree_count']
                except:
                    digg_count = 0
                user_name = hot_comment[0]['nick']
                head_url = hot_comment[0]['head_url']
                info = {
                    'originId':hot_comment[0]['reply_id'],
                    'content': comment_text,
                    'publishTime': create_time,
                    'likeNum': digg_count,
                    'username': user_name,
                    'avatar': head_url,
                    # 'replies': [],
                }
                reply_id = hot_comment[0]['reply_id']
                if reply_id in reply_ids:
                    pass
                if num >= 5:
                    break
                # else:
                #     reply_ids.append(reply_id)
                #     num += 1
                #     url = "https://r.cnews.qq.com/getQQNewsOrigReplyComment"
                #     old_reply_id = ''
                #     payload = "orig_id={}&old_reply_id={}&comment_id={}".format(reply_id, old_reply_id, comment_id)
                #     response = requests.post(url, data=payload, headers=headers, verify=False).text
                #     ob_json = json.loads(response)
                #     # reply_count = int(ob_json['comments']['orig']['reply_num'])
                #     old_reply_id = ''
                #     payload = "orig_id={}&old_reply_id={}&comment_id={}".format(reply_id, old_reply_id, comment_id)
                #     response = requests.post(url, data=payload, headers=headers, verify=False).text
                #     ob_json = json.loads(response)
                #     try:
                #         for reply in ob_json['comments']['reply_list']:
                #             if reply[0]['reply_id'] in reply_ids2:
                #                 pass
                #             if count >= 20:
                #                 break
                #             else:
                #                 reply_ids2.append(reply[0]['reply_id'])
                #                 reply_text = reply[0]['reply_content']
                #                 reply_create_time = int(reply[0]['pub_time'])
                #                 try:
                #                     digg_count = reply[0]['agree_count']
                #                 except:
                #                     digg_count = 0
                #                 name = reply[0]['nick']
                #                 head_url = reply[0]['head_url']
                #                 count += 1
                #                 reply_info = {
                #                     'originId':reply[0]['reply_id'],
                #                     'content': reply_text,
                #                     'publishTime': reply_create_time,
                #                     'likeNum': digg_count,
                #                     'username': name,
                #                     'avatar': head_url,
                #                 }
                #                 rep.append(reply_info)
                #         info['replies'] = rep
                #         break
                #     except:
                #         pass
                comments.append(info)
        except Exception as e:
            is_post = False
            logging.error(str(e))
        self.result['comments'] = comments
        return is_post









