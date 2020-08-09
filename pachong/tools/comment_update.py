from tools.RedisQueue import RedisQueue
from tools.myrequests import _requests as requests
import json
import logging
import time

kuaibao_comment = RedisQueue('kuaibao')
toutiao_comment = RedisQueue('toutiao')


commentupdate_api = 'http://qmtest.newtvmall.com/api/import/news/lessComment'

def get_commentupdate():
    response = requests.get(commentupdate_api)
    ob_json = json.loads(response.text)
    num = 0
    for comment in ob_json['data']:
        num += 1
        if 'toutiao' in comment['url']:
            toutiao_comment.put(comment)
            print('已添加{}'.format(comment['url']))
            print(num)
        else:
            kuaibao_comment.put(comment)
            print('已添加{}'.format(comment['url']))
            print(num)



def main():
    while True:
        try:
            get_commentupdate()
            time.sleep(30)
        except Exception as e:
            logging.error('Connect Error!!!', e)



if __name__ == '__main__':
    get_commentupdate()