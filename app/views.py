from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.email import send_email
from app.forms import LoginForm, RegisterForm, ForgetPasswordForm
from app.models import User


@app.before_request
def before_requset():
    if current_user.is_authenticated and not current_user.confirm \
            and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('unconfirmed'))


@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirm:
        return redirect(url_for('index'))
    return render_template('auth/unconfirmed.html')


@app.route('/register/unconfirmed')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/confirm', user=current_user, token=token)
    flash('A new confirmation email has been posted to you.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data is not form.confirm.data:
            flash('Password does not equals to Confirm.')
        else:
            flash('You will receive an email, and click the link in it.')
            username = User(nickname=form.nickname, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = username.generate_confirmation_token()
            send_email(username.email, 'Confirm your account', 'auth/confirm', user=username, token=token)
            flash(message='A confirmation email has been sent to your mailbox.')
            return redirect(url_for('index'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/register/confirm/<token>')
@login_required
def register_confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('Register success!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('user.html'))
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(nickname=form.nickname.data).first()
        if username is not None:
            if username.verify_password(form.password.data):
                # Login and validate the user.
                # user should be an instance of your `User` class
                flash('Login success!')
                login_user(username, form.remember_me.data)

                next = request.args.get('next')
                # next_is_valid should check if the user has valid
                # permission to access the `next` url
                #if not next_is_valid(next):
                #    return abort(400)
                return redirect(next or url_for('index'))
            else:
                flash('Password is incorrect. Please check and modify it.')
        else:
            flash(form.nickname.data+' is not existed.')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(message='You have been logged out.')
    return redirect(url_for('login'))


@app.route('/forget_password')
def forget_password():
    form = ForgetPasswordForm()
    return render_template('auth/forget_password.html',title='Forget Password', form=form)


@app.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html', title='Contact Us')


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        abort(404)
    else:
        return render_template('main/user.html', title='Welcome', user=user)


@app.route('/', methods=['GET'])
@login_required
def index():
    return redirect('/user/' + current_user.nickname)
