#!/home/flask_learn/flask/bin/python
# encoding: utf-8

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    hash_psw = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)     # python 3

    def generate_psw(self, password):
        self.hash_psw = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_psw, password)

    def avatar(self, size):
#        return 'http://www.gravatar.com/avatar' + md5(str(self.id)).hexdigest() + '?d=mm&s=' + str(size)
        return 'http://7xpqi6.com1.z0.glb.clouddn.com/avatar' + str(int(self.id)%23 + 6) + '.png-size' + str(size)




    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
