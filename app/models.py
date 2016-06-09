#!/home/flask_learn/flask/bin/python
# encoding: utf-8

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from hashlib import md5
from markdown import markdown
import bleach

from app import app
import sys

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy as whooshalchemy

followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
        )

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirm = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    hash_psw = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    api_key = db.Column(db.String(40))
    followed = db.relationship(
            'User',
            secondary = followers,
            primaryjoin = (followers.c.follower_id == id),
            secondaryjoin = (followers.c.followed_id == id),
            backref = db.backref('followers', lazy='dynamic'),
            lazy = 'dynamic'
            )

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

    def generate_api_key(self):
        self.api_key = hashlib.sha1(str(self.id) + app.config['SALT']).hexdigest()

    def verify_password(self, password):
        return check_password_hash(self.hash_psw, password)

    def avatar(self, size):
#        return 'http://www.gravatar.com/avatar' + md5(str(self.id)).hexdigest() + '?d=mm&s=' + str(size)
        return 'http://7xpqi6.com1.z0.glb.clouddn.com/avatar' + str(int(self.id)%23 + 6) + '.png-size' + str(size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count()>0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id==self.id).order_by(Post.timestamp.desc())

    def user_to_json(self):
        json_user = {
                "user_id": self.id,
                "nickname": self.nickname,
                "about_me": self.about_me,
                "last_seen": self.last_seen
                }
        return json_user


    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a','abbr','acronym','b','blockqoute','code','em','i','li','ol','pre','strong','ul','h1','h2','h2','h3','p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Essay No.%d>' % (self.id)

if enable_search:
    whooshalchemy.whoosh_index(app, Post)














