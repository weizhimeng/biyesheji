# -***coding=utf-8***-
# zaj_forms.py,存放表单操作
from flask_wtf import FlaskForm
# 每个Web表单都由一个继承自FlaskForm的类表示
from wtforms import StringField,PasswordField,SubmitField
# StringField类表示的是属性为type="text"的<input>元素。
# SubmitField类表示的是是属性为type="submit"的<input>元素

#WTForms内建的验证函数validators,而且是以数组形式，正对应了前面说的一个字段可以有一个或者多个验证函数
from wtforms.validators import Length, Required, EqualTo, Regexp,Email


class LoginForm(FlaskForm):
    user = StringField(
        label='用户名',
        validators=[
            Length(1,13)
        ]
    )
    passwd = PasswordField(
        label='密码',
        validators=[
            Length(1,12),
        ]
    )
    submit = SubmitField(
        label='登陆'
    )
class RegisterFrom(FlaskForm):
    user = StringField(
        label='用户名/邮箱/手机号',
        validators=[
            Length(1,13)
        ]
    )
    passwd = PasswordField(
        label='密码',
        validators=[
            Length(1,12),
        ]
    )
    repasswd = PasswordField(
        label='确认密码',
        validators=[
            EqualTo('passwd',message='密码不一致！')
        ]
    )
    # phone = StringField(
    #     label='电话号码',
    #     validators=[
    #         Regexp(r'1\d{10}', message='手机号码格式错误')
    #     ]
    # )
    # email = StringField(
    #     label='邮箱',
    #     validators=[
    #         Email(message='邮箱格式错误！')
    #     ]
    # )
    submit = SubmitField(
        label='注册'
    )