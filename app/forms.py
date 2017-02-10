from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[PasswordField])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField()


class RegisterForm(FlaskForm):
    nickname = StringField(u'昵称', validators=[DataRequired])
    email = StringField(u'邮箱', validators=[DataRequired, Email()])
    password = PasswordField(u'密码', validators=[DataRequired, Length(6, 12, message=u'密码长度在6到12为')])
    password1 = PasswordField(u'确认密码', validators=[DataRequired, Length(6, 12, message=u'密码长度在6到12为'),EqualTo('password', message=u'密码必须一致')])
    submit = SubmitField(u'注册')