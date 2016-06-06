#!/home/flask_learn/flask/bin/python
# encoding:utf-8

from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm, RegisterForm, EditForm, PostForm, SearchForm
from models import User, Post
from flask_login import login_user, logout_user, current_user,login_required
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/index/<int:page>", methods=['GET', 'POST'])
@login_required
def index(page=1):
    user = g.user
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live !')
        return redirect(url_for('index'))
#    posts = g.user.followed_posts().all()
#    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False).items
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
#    return render_template("index.html", user=user)
#    return render_template("index.html", title="Home", user=user)
    return render_template("index.html", title="Home",user=user,form=form, posts=posts)

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
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
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
        # 全文搜索
        g.search_form = SearchForm()

# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 用户页面
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User' + nickname + 'not found.')
        return redirect(url_for("index"))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template("user.html", user=user, posts=posts)

# 编辑个人信息
@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
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

# 定制HTTP错误处理器
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# 关注
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow youself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + "!")
    return redirect(url_for('user', nickname=nickname))

# 取消关注
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow youself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))

# 搜索
@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)





































@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    form = EmailForm()
    if form.validate_on_submit():
        g.user.email = form.email.data
        g.user.email_comfirm = False
        db.session.add(g.user)
        db.session.commit()
        subject = u'[Bavel]确认邮箱，此邮件不需要回复'
        token_str = '~'.join([form.email.data, g.user.nickname])
        token = ts.dumps(token_str)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        send_email(form.email.data, subject, 'mail/confirm', user=g.user, confirm_url=confirm_url)
        flash(u'确认邮件已发送至邮箱，请查收')
        return redirect(url_for('index'))
    return render_template('account.html',user=g.user, form=form)












