#!/home/flask_learn/flask/bin/python
# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from app.models import User, Post

#class LoginForm(Form):
#    openid = StringField('openid', validators=[DataRequired()])
#    remember_me = BooleanField("remember_me", default=False)

class LoginForm(Form):
    nickname = StringField('nickname', validators=[Length(min=1,max=20,message=u'昵称长度为1-20个字符')])
    password = PasswordField('password', validators=[Length(min=4,max=20,message=u'密码长度为4-20个字符')])
    remember_me = BooleanField("remember_me", default=True)

    def validate_nickname(form,field):
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user == None:
            field.errors.append(u'用户名不存在！')
            return False
        return True

    def validate_password(form, field):
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user == None:
            return False
        if not user.verify_password(field.data):
            field.errors.append(u'密码错误')
            return False
        return True

class RegisterForm(Form):
    nickname = StringField('nickname', validators=[Length(min=1, max=20, message=u'昵称长度为1-20个字符')])
    password = PasswordField('password', validators=[Length(min=4, max=20, message=u'密码长度为4-20个字符'), EqualTo('confirm', message=u'两次输入必须相同')])
    confirm = PasswordField('Repeat Password')

    def validate_nickname(form, field):
        user = User.query.filter_by(nickname=field.data).first()
        if user is not None:
            field.errors.append(u'这个昵称已经被使用了～')
            return False
        return True

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0,max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])







