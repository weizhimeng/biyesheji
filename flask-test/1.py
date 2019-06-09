# -***coding=utf-8***-
from tool.db import connect,find,findall,connect_user
from tool.redisdb import RedisQueue
from tool.db import connect,findall,connect_recommend,find,connect_history

import matplotlib.pyplot as plt

# def fun(user):
#     user_db = connect_user()[user]
#     keys = findall(user_db)[0]['keys']
#     print(keys)
#     count = 0
#     for i in keys.keys():
#         count += 1
#     print(count)
#     # user_db.update_one({'keys':keys}, {"$set":{'keys':{'a':2,'b':1}}})
#
#
# queue = RedisQueue('new')
# if queue.empty():
#     print('none')
# else:
#     result = queue.get()
#     print(result)
import matplotlib as mpl
mpl.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
mpl.rcParams['axes.unicode_minus'] = False

# x = ['1','2','3','4','5']
# y = [8.19,8.14,8.07,8.28,7.98]
# a = [6.72,6.61,6.67,6.24,6.33]
# b = [5.22,5.13,4.98,5.14,4.95]
# plt.figure(figsize=(8,4)) #创建绘图对象
# plt.plot(x,y,"b-",linewidth=1,label='0.5',color='blue')   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
# plt.plot(x,a,"b--",linewidth=1,label='0.4',color='red')
# plt.plot(x,b,"b-.",linewidth=1,label='0.3',color='green')
# plt.xlabel("day/天") #X轴标签
# plt.ylabel("score/分")  #Y轴标签
# plt.title("") #图标题
# plt.legend()
# plt.show()  #显示图
# plt.savefig("line.jpg") #保存图


x = ['1.5','1.6','1.7','1.8','1.9','1.10','1.11']
y = [6574,5764,5976,6312,6084,5970,6130]
plt.figure(figsize=(8,4)) #创建绘图对象
plt.plot(x,y,"b-",linewidth=1,label='抓取条数',color='blue')   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.xlabel("日期") #X轴标签
plt.ylabel("条数/条")  #Y轴标签
plt.title("") #图标题
plt.legend()
plt.show()  #显示图
plt.savefig("line.jpg") #保存图
