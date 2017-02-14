from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[PasswordField])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField()


class RegisterForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired])
    email = StringField('email', validators=[DataRequired, Email()])
    password = PasswordField('password', validators=[DataRequired, Length(6, 12, message=u'密码长度在6到12位')])
    confirm = PasswordField('confirm', validators=[DataRequired, Length(6, 12, message=u'密码长度在6到12位'),\
                                                   EqualTo('password', message=u'密码必须一致')])
    submit = SubmitField('register')
