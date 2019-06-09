# -***coding=utf-8***-
from flask import Flask,render_template,session,redirect,url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm,RegisterFrom
from models import isPasswdOk,addUser
import  functools
from tool.db import connect,findall
app = Flask(__name__)

app.config['SECRET_KEY'] = 'SHEEN'
bootstrap = Bootstrap(app)

mydb = connect().value
datas = findall(mydb)
data = list(datas[:100])

def fun(db):
    mydb = connect()[db]
    news = findall(mydb)
    news = list(news[:100])
    return news

# def is_login(f):
#     """判断用户是否登陆的装饰器"""
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         # 主函数代码里面， 如果登陆， session加入user， passwd两个key值；
#         # 主函数代码里面， 如果注销， session删除user， passwd两个key值；
#         # 如果没有登陆成功， 则跳转到登陆界面
#         if 'user' not in session:
#             return  redirect('/login/')
#         # 如果用户是登陆状态， 则访问哪个路由， 就执行哪个路由对应的视图函数；
#         return  f(*args, **kwargs)
#     return  wrapper

@app.route('/')
def index():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'shouye','user':user})

@app.route('/tuijian')
def tuijian():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'','user':user})
@app.route('/own/<user>/')
def own(user):
    return render_template('index.html',cat={'cat':'','user':user})

@app.route('/yule')
def yule():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'yule','user':user})

@app.route('/keji')
def keji():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'keji','user':user})

@app.route('/dongman')
def dongman():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'dongman','user':user})

@app.route('/lishi')
def lishi():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'lishi','user':user})

@app.route('/guoji')
def guoji():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'guoji','user':user})

@app.route('/tiyu')
def tiyu():
    try:
        user = session['user']
    except:
        user = ''
    return render_template('index.html',cat={'cat':'tiyu','user':user})


@app.route('/login/',methods=['GET','POST'])
def login():
    form  = LoginForm()
    if form.validate_on_submit():
        user = form.data['user']
        passwd = form.data['passwd']
        if isPasswdOk(user,passwd):
            session['user'] = user
            session['passwd'] = passwd
            return redirect(url_for('index'))
        else:
            return render_template('login.html',form=form,message='密码或用户名错误')
    else:
        return render_template('login.html',form=form)

@app.route('/register/',methods=['GET','POST'])
def register():
    form = RegisterFrom()
    # 如果是post方法并且表单验证通过的话， 返回True;
    if form.validate_on_submit():
        # 用户提交的表单信息
        print(form.data)
        addUser(form.data['user'],form.data['passwd'])
        return redirect(url_for('index'))
        # return 'ok'
    return  render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('passwd', None)
    # 注销即删除用户的session信息， 注销成功， 跳转到首页;
    return  redirect(url_for('index'))
    # return  redirect('/')

if __name__ == '__main__':
    app.run( debug=True,port=8000)
