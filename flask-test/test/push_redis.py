# -***coding=utf-8***-
#将用户数据库内推荐数据传入redis
from tool.redisdb import RedisQueue
from tool.db import connect,findall,connect_recommend,find,connect_history

def push_data(username):
    queue = RedisQueue(username)
    mydb = connect_recommend()[username]
    datas = findall(mydb)
    user_history = connect_history()[username]
    for data in datas:
        url = data['url']
        res = list(find(user_history, {'url': url}))
        if res == []:
            queue.put(data)


# user_db = connect().users
# users = findall(user_db)
# for user in users:
#     user = user['username']
#     queue = RedisQueue(user)
#     push_data(user)



if __name__ == '__main__':
    push_data('kkkk')
