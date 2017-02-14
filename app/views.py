from app import app
from flask import render_template, flash, redirect, url_for
from .forms import LoginForm, RegisterForm
from app.models import User
from flask_mail import Mail


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                flash('Login requested for '+form.nickname.data)
                return redirect(url_for('index'))
            flash('Password is incorrect. Please check and modify it.')
        flash(form.nickname.data+' is not existed.')
        return redirect(url_for('register'))
    flash('Login success!')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password is not form.confirm:
            flash('Password does not equals to Confirm.')
        flash('You will receive an email, and click the link in it.')
        user = User(nickname=form.nickname, email=form.email.data, password=form.password.data)
        db.sesssion.add(user)
        db.sesssion.commit()
    flash('Register success!')
    return render_template('register.html', form=form)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
