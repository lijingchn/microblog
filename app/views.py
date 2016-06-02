#!/home/flask_learn/flask/bin/python
# encoding:utf-8

from app import app
from flask import render_template, flash, redirect
from forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
#    return "Hello, World."
    user = {'nickname':'lijing'}
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
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for OpenID = " + form.openid.data +" "+ str(form.remember_me.data))
        return redirect("/index")
    return render_template("login.html", title="Sign In", form=form)

