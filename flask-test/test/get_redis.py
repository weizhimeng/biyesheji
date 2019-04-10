# -***coding=utf-8***-
#从redis中获取推荐数据，一次请求5条
from flask import Flask,render_template,session,redirect,url_for,jsonify,request
from tool.redisdb import RedisQueue
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/getdata',methods=['POST'])
def index():
    user = request.form['user']
    cat = request.form['cat']
    if cat == '':
        user = user
    else:
        user = cat
    queue = RedisQueue(user)
    results = []
    for i in range(5):
        result = queue.get()
        data = eval(result)
        results.append(data)
    print(len(results))
    return jsonify(results)

if __name__ == '__main__':
    app.run( debug=True)