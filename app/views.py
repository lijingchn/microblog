#!/home/flask_learn/flask/bin/python
# encoding:utf-8

from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm, RegisterForm, EditForm
from models import User
from flask_login import login_user, logout_user, current_user,login_required
from datetime import datetime



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
def login():
    if (g.user is not None) and (g.user.is_authenticated):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        session['remember_me'] = form.remember_me.data
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user,remember=remember_me)
        return redirect('/index')
#        return oid.try_login(form.openid.data, ask_for=['nickname','email'])
#        flash("Login requested for OpenID = " + form.openid.data +" "+ str(form.remember_me.data))
    return render_template("login.html", title="Sign In", form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data)
        user.generate_psw(form.password.data)
        db.session.add(user)
        db.session.commit()
#        db.session.add(user.follow(user))
#        db.session.commit()
        flash(u'成功注册！')
        login_user(user)
        return redirect('index')
    return render_template('register.html', title='Sign Up', form=form)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

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

# 编辑个人信息
@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit"))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template("edit.html", form=form)












