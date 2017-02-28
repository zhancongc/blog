# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, abort, current_app, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm, EditProfileForm, NewArticleFrom
from app.models import User, Article
from .email import send_email

auth = Blueprint('auth', __name__, template_folder='templates/auth')
art = Blueprint('art', __name__, template_folder='templates/article')
user = Blueprint('user', __name__, template_folder='templates/user')
foll = Blueprint('foll', __name__, template_folder='templates/follow')


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).limit(100).paginate(page, per_page=current_app.config[\
        'FLASK_ARTICLE_PER_PAGE'], error_out=False)
    articles = pagination.items
    return render_template('index.html', title=u'最新文章', articles=articles, pagination=pagination, display=0)


@app.route('/about')
def about():
    return render_template('about.html', title=u'联系方式')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        db.session.add(username)
        db.session.commit()
        token = username.generate_confirmation_token()
        send_email(username.email, u'邮箱验证', 'auth/confirm', user=username, token=token)
        flash(u'您将会收到一封确认邮件，请点击其中的链接')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=u'注册', form=form)


@auth.route('/register/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('index'))
    return render_template('unconfirmed.html', title=u'邮箱验证')


@auth.route('/register/resend_email', methods=['GET', 'POST'])
def resend_email():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        username = User.query.filter_by(email=form.email.data).first()
        token = username.generate_confirmation_token()
        send_email(username.email, u'验证您的邮箱', 'confirm', user=username, token=token)
        flash(u'您将会收到一封确认邮件，请点击其中的链接')
        return redirect(url_for('index'))
    return render_template('resend_email.html', title=u'发送确认邮件', form=form)


@auth.route('/register/confirm/<token>')
@login_required
def register_confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash(u'注册成功')
    else:
        flash(u'该链接非法或已经失效')
    current_user.confirmed = True
    db.session.commit()
    return redirect(url_for('user.profile', nickname=current_user.nickname))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('user.profile', nickname=current_user.nickname))
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(email=form.email.data).first()
        if username is not None:
            if username.verify_password(form.password.data):
                # Login and validate the user.
                # user should be an instance of your `User` class
                flash(u'登陆成功')
                login_user(username, form.remember_me.data)

                next = request.args.get('next')
                # next_is_valid should check if the user has valid
                # permission to access the `next` url
                # if not next_is_valid(next):
                #    return abort(400)
                return redirect(next or url_for('index'))
            else:
                flash(u'密码错误，请您检查用户名或密码是否正确')
        else:
            flash(u'账户' + form.email.data + u'不存在')
    return render_template('login.html', title=u'登陆', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(message=u'您已注销')
    return redirect(url_for('index'))


@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        username = User.query.filter_by(email=form.email.data).first()
        token = username.generate_confirmation_token()
        send_email(username.email, u'验证您的邮箱', 'forget_password', user=username, token=token)
        return redirect(url_for('index'))
    return render_template('forget_password.html', title=u'忘记密码', form=form)


@auth.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_password(token):
    email = request.args.get('email')
    username = User.query.filter_by(email=email).first()
    if username.confirm(token):
        form = ResetPasswordForm()
        if form.validate_on_submit():
            if form.password.data == form.confirm.data:
                username.password = form.password.data
                db.session.commit()
                flash(u'新密码已生效')
                return redirect(url_for('auth.login'))
        return render_template('auth.reset_password.html', title=u'密码重置', form=form)
    else:
        flash(u'该链接非法或已经失效')


@user.route('/profile/<nickname>')
def profile(nickname):
    username = User.query.filter_by(nickname=nickname).first()
    if username is None:
        abort(404)
    articles = Article.query.filter_by(author_id=username.id).order_by(Article.timestamp.desc()).limit(3)
    return render_template('profile.html', title=u'个人信息', user=username, articles=articles)


@user.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.city = form.city.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(message=u'您的个人信息已经成功更新了')
        return redirect(url_for('user.profile', nickname=current_user.nickname))
    form.nickname.data = current_user.nickname
    form.city.data = current_user.city
    form.about_me.data = current_user.about_me
    return render_template('profile_edit.html', title=u'编辑个人信息', form=form)


@art.route('/my')
@login_required
def user_article():
    articles = Article.query.filter_by(author_id=current_user.id).order_by(Article.timestamp.desc()).all()
    return render_template('user_article.html', title=u'我的文章', articles=articles, display=0)


@art.route('/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', title=u'文章', articles=[article], display=1)


@art.route('/new', methods=['GET', 'POST'])
@login_required
def new_article():
    form = NewArticleFrom()
    if form.validate_on_submit():
        article = Article(title=form.title.data, body=form.body.data, author_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('art.user_article'))
    return render_template('new.html', title=u'发文章', form=form, display=1)


@art.route('/edit/<int:id>', methods=['GET', 'POST'])
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
        flash(u'您的文章已经成功更新了')
        return redirect(url_for('art.article', id=article.id))
    form.title.data = article.title
    form.body.data = article.body
    return render_template('edit.html', title=u'编辑文章', form=form, id=article.id, display=1)


@foll.route('/follow/<nickname>')
@login_required
def follow(nickname):
    username = User.query.filter_by(nickname=nickname).first()
    if username is None:
        flash(u'无效用户名')
        return redirect(url_for('index'))
    if current_user.is_following(username):
        flash(u'您无需重复关注')
        return redirect(url_for('user.profile', nickname=nickname))
    current_user.follow(username)
    flash(u'您已经关注了 %s.' % nickname)
    return redirect(url_for('user.profile', nickname=nickname))


@foll.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    username = User.query.filter_by(nickname=nickname).first()
    if username is None:
        flash(u'无效用户名')
        return redirect(url_for('index'))
    if not current_user.is_following(username):
        flash(u'您之前并未关注 %s' % nickname)
        return redirect(url_for('user.profile', nickname=nickname))
    current_user.unfollow(username)
    flash(u'您已经取消关注了 %s' % nickname)
    return redirect(url_for('user.profile', nickname=nickname))


@foll.route('/followers/<nickname>')
def followers(nickname):
    username = User.query.filter_by(nickname=nickname).first()
    if username is None:
        flash(u'无效的用户名')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = username.followers.paginate(page, per_page=current_app.config['FLASK_FOLLOW_PER_PAGE'], error_out=False)
    followers = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=username, title=u"关注ta的人", endpoint='foll.followers',\
                           pagination=pagination,  followers=followers)


@foll.route('/followed_by/<nickname>')
def followed_by(nickname):
    username = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(u'无效的用户名')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = username.followed.paginate(page, per_page=current_app.config['FLASK_FOLLOW_PER_PAGE'], error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followed_by.html', user=username, title=u"ta关注的人", endpoint='foll.followed_by',\
                           pagination=pagination,  follows=follows)
