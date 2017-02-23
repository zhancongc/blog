# coding = utf-8

from flask import render_template, flash, redirect, url_for, request, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, mail
from flask_mail import Message
from app.forms import LoginForm, RegisterForm, ForgetPasswordForm, EditProfileForm, NewArticleFrom
from app.models import User, Article
from .email import send_email
from random import randint


@app.before_request
def before_requset():
    if current_user.is_authenticated and not current_user.confirm \
            and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('unconfirmed'))


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(\
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    articles = pagination.items
    return render_template('main/index.html', title='最新文章',\
                           articles=articles, pagination=pagination, display=0)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        db.session.add(username)
        db.session.commit()
        token = username.generate_confirmation_token()
        send_email(username.email, '邮箱验证', 'auth/confirm', user=username, token=token)
        flash('您将会收到一封确认邮件，请点击其中的链接')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='注册', form=form)


@app.route('/register/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirm:
        return redirect(url_for('index'))
    return render_template('auth/unconfirmed.html', title='警告')


@app.route('/register/resend_email')
@login_required
def resend_email():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '验证您的邮箱',\
               'auth/confirm', user=current_user, token=token)
    flash('您将会收到一封确认邮件，请点击其中的链接')
    return redirect(url_for('index'))


@app.route('/register/confirm/<token>')
@login_required
def register_confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('注册成功')
    else:
        flash('该链接非法或已经失效')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('user'))
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(email=form.email.data).first()
        if username is not None:
            if username.verify_password(form.password.data):
                # Login and validate the user.
                # user should be an instance of your `User` class
                flash('登陆成功')
                login_user(username, form.remember_me.data)

                next = request.args.get('next')
                # next_is_valid should check if the user has valid
                # permission to access the `next` url
                # if not next_is_valid(next):
                #    return abort(400)
                return redirect(next or url_for('index'))
            else:
                flash('密码错误，请检查用户名或密码是否正确')
        else:
            flash(form.email.data+' is not existed.')
    return render_template('auth/login.html', title='登陆', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(message='您已注销')
    return redirect(url_for('login'))


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        rand = randint(1000,9999)
        msg = Message('Confirm code', sender='1227753320@qq.com', recipients=form.email.data)
        msg.body = '验证码是' + str(rand) + '.'
        with app.app_context():
            mail.send(msg)
        return redirect(url_for('index'))
    return render_template('auth/forget_password.html', title='忘记密码', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    pass


@app.route('/about')
def about():
    return render_template('main/about.html', title='联系方式')


@app.route('/profile/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        abort(404)
    return render_template('user/profile.html', title='个人信息', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.city = form.city.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(message='您的个人信息已经成功更新了')
        return redirect(url_for('user', nickname=current_user.nickname))
    form.nickname.data = current_user.nickname
    form.city.data = current_user.city
    form.about_me.data = current_user.about_me
    return render_template('user/profile_edit.html', title='编辑个人信息', form=form)


@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article/article.html', title='文章', articles=[article], display=1)


@app.route('/articles/user')
@login_required
def user_article():
    articles = Article.query.filter_by(author_id=current_user.id).order_by(Article.timestamp.desc()).all()
    return render_template('article/user_article.html', title='我的文章', articles=articles, display=0)


@app.route('/articles/new', methods=['GET', 'POST'])
@login_required
def new_article():
    form = NewArticleFrom()
    if form.validate_on_submit():
        article = Article(title=form.title.data, body=form.body.data, author_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user_article'))
    return render_template('article/new.html', title='发文章', form=form, display=1)


@app.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if current_user.id is not article.author_id:
        abort(403)
    form = NewArticleFrom()
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        db.session.add(article)
        flash('您的文章已经成功更新了')
        return redirect(url_for('article', id=article.id))
    form.title.data = article.title
    form.body.data = article.body
    return render_template('article/edit.html', title='编辑文章', form=form, id=article.id, display=1)
