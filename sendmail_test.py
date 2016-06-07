#!/home/flask_learn/flask/bin/python
# encoding: utf-8
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '337859457@qq.com'
app.config['MAIL_PASSWORD'] = 'quergtfjoyzybjgi'

mail = Mail(app)
msg = Message(u'邮件主题', sender='337859457@qq.com', recipients=['lijingjing.chn@gmail.com'])
msg.body = u'邮件内容'
msg.html = u"<h1>邮件的html模板<h1> body"

with app.app_context():
    mail.send(msg)

