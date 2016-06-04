#!/home/flask_learn/flask/bin/python
# encoding:utf-8

from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm
from models import User
from flask_login import login_user, logout_user, current_user,login_required



@app.route("/")
@app.route("/index")
@login_required
def index():
#    return "Hello, World."
    user = g.user
    posts = [
            # fake array of posts
            {
                'author':{'nickname':'lijing'},
                'body':'Beautiful day in Portland!'
                },
            {
                'author':{'nickname':'Susan'},
                'body':'The Avengers movie was so cool!'
                }
            ]
#    return render_template("index.html", user=user)
#    return render_template("index.html", title="Home", user=user)
    return render_template("index.html", title="Home",user=user, posts=posts)

@app.route("/login", methods=['GET','POST'])
@oid.loginhandler
def login():
    if (g.user is not None) and (g.user.is_authenticated):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname','email'])
#        flash("Login requested for OpenID = " + form.openid.data +" "+ str(form.remember_me.data))
    return render_template("login.html", title="Sign In", form=form, providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email=="":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.neckname
        if nickname is None or nickname=="":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 用户页面
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User' + nickname + 'not found.')
        return redirect(url_for("index"))
    posts = [
            {'author':user, 'body':'Test post #1'},
            {'author':user, 'body':'Test post #2'},
            ]
    return render_template("user.html", user=user, posts=posts)













