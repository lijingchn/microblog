#!/home/flask_learn/flask/bin/python
# encoding: utf-8

from flask_mail import Message, Mail
from flask import render_template, current_app
from app import mail
from app import app
from threading import Thread
#from decorators import async

#@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr




