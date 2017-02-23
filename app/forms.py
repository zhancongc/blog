from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_pagedown.fields import PageDownField


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField()


class RegisterForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(6, 12)])
    confirm = PasswordField('confirm', validators=[DataRequired(), Length(6, 12), EqualTo('password')])
    submit = SubmitField('submit')


class ForgetPasswordForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('send')


class ResetPasswordForm(FlaskForm):
    password = StringField('new password', validators=[DataRequired()])
    confirm = StringField('confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')


class EditProfileForm(FlaskForm):
    nickname = StringField('nickname', validators=[Length(0,64)])
    city = StringField('city', validators=[Length(0,64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('submit')


class NewArticleFrom(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    body = PageDownField('body', validators=[DataRequired()],\
                         render_kw={'rows': 14, 'placeholder': 'write something freely'})
    # body = TextAreaField('body', validators=[DataRequired('null is not allowed.')],\
    #                     render_kw={'rows': 14, 'placeholder': 'write something freely'})
    submit = SubmitField('submit')

