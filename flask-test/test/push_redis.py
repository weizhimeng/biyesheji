# -***coding=utf-8***-
#将用户数据库内推荐数据传入redis
from tool.redisdb import RedisQueue
from tool.db import connect,findall,connect_recommend

def push_data(queue,mydb):
    count = 0
    datas = findall(mydb)
    for data in datas:
        queue.put(data)
        count += 1
    print(count)


user_db = connect().users
users = findall(user_db)
for user in users:
    user = user['username']
    queue = RedisQueue(user)
    u = connect_recommend()[user]
    push_data(queue,u)



if __name__ == '__main__':
    queue = RedisQueue('root')
    mydb = connect_recommend().root
    push_data(queue,mydb)