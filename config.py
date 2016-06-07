#!/home/flask_learn/flask/bin/python
# encoding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587                #国内的邮箱代理基本上端口都是25,但是国外的比如gmail可能有所不同，具体需要上网查询
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = '337859457@qq.com'       #你的邮箱帐号，不需要@以及后面的部分
MAIL_PASSWORD = 'quergtfjoyzybjgi'       #你的邮箱密码

# administrator list
MAIL_DEFAULT_SENDER = [u'Microblog Team', '337859457@qq.com']
FLASKY_MAIL_SUBJECT_PREFIX = '[Microblog]'

# pagination
POSTS_PER_PAGE = 6

# Set up full-text search database
WHOOSH_BASE = os.path.join(basedir,'search.db')
MAX_SEARCH_RESULTS = 50
MAX_INT = 10000

# Internationalization
# available languages
LANGUAGES = {
        'en':'English',
        'es':'Español'
        }
