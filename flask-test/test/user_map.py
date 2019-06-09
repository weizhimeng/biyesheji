# -***coding=utf-8***-
#接受浏览记录，更新用户关键词的值
from flask import Flask,render_template,session,redirect,url_for,request,jsonify
from tool.db import connect,find,findall,connect_user,connect_history
import pymongo
# user_db = connect().news_keys
# user_db.ensure_index('url', unique=True)
# exit()
app = Flask(__name__)

@app.route('/usermap',methods=['POST'])
def index():
    # data 为关键词字典
    # user = request.form['user']
    # url = request.form['url']
    # user_db = connect().news_keys
    # print(url)
    # data = list(find(user_db, {'url':url}))
    # print(data[0]['keywords'])
    # return jsonify(request.form['user'])
    try:
        user = request.form['user']
        url = request.form['url']
        user_history = connect_history()[user]
        res = list(find(user_history, {'url': url}))
        if res == []:
            user_history.insert({'url': url})
        news_db = connect().news_keys
        print(url)
        data = list(find(news_db, {'url': url}))[0]['keywords']
        print(data)
        user_db = connect_user()[user]
        try:
            keys = findall(user_db)[0]['keys']
        except:
            user_db.insert({'keys':{}})
            keys = findall(user_db)[0]['keys']
        for key in data.keys():
            if key in keys.keys():
                if float(data[key]) > float(keys[key]):
                    keys[key] = float(data[key]) + float(keys[key]) * 0.2
                else:
                    keys[key] = float(keys[key]) + float(data[key]) * 0.2
            else:
                keys[key] = data[key]
        # user_db.update_one(findall(user_db)[0]['keys'], keys)
        print(keys)
        user_db.update_one({'keys': findall(user_db)[0]['keys']}, {"$set": {'keys': keys}})
        return jsonify({'sucess': 1})
    except:
        return jsonify({'sucess': 0})
if __name__ == '__main__':
    app.run( debug=True,port=7000)



