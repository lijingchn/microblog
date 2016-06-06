#!/home/flask_learn/flask/bin/python
# encoding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"

OPENID_PROVIDERS = [
        {'name':'Google', 'url':'https://www.google.com/accounts/o8/id'},
        { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
        { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
        { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
        { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
        ]

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['337859457@qq.com']

# pagination
POSTS_PER_PAGE = 3

# Set up full-text search database
WHOOSH_BASE = os.path.join(basedir,'search.db')
MAX_SEARCH_RESULTS = 50
