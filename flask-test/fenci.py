# -***coding=utf-8***-
import jieba
import jieba.analyse
from pymongo import MongoClient


def connect():
    client = MongoClient('localhost', 27017)
    db = client.test
    return db
def findall(collection):
    return collection.find()

def tfidf(string):
    return dict(jieba.analyse.extract_tags(string, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns')))


news = connect().news
news_keys = connect().news_keys
data = findall(news)
count = 0
for d in data:
    result = []
    count += 1
    for data in d['data'][0]['contentItems']:
        if data['type'] == 'text':
            result.append(data['content'])
    result = ''.join(result)
    if len(result) >300:
        d['keywords'] = tfidf(result)
        d['_id'] = d['url']
        if news_keys.find_one({'url':d['url']}):
            print('exist')
            news.delete_one({'url': d['url']})
        else:
            news_keys.insert(d)
            news.delete_one({'url': d['url']})
    print(count)
    news.delete_one({'url': d['url']})