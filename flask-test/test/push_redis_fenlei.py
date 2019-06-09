# -***coding=utf-8***-
#将用户数据库内推荐数据传入redis
from tool.redisdb import RedisQueue
from tool.db import connect,findall

def push_data(queue,mydb):
    count = 0
    datas = findall(mydb)
    for data in datas:
        count += 1
        queue.put(data)
        if count >= 1000:
            break


def run(cat):
    queue = RedisQueue(cat)
    mydb = connect()[cat]
    push_data(queue, mydb)

if __name__ == '__main__':
    queue = RedisQueue('shouye')
    mydb = connect().news_keys
    push_data(queue, mydb)
    # run('user')
    # for i in ['yule','keji','dongman','tiyu','guoji','lishi']:
    #     run(i)