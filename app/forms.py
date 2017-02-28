# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_pagedown.fields import PageDownField


class LoginForm(FlaskForm):
    email = StringField(u'账号', validators=[DataRequired(u'请填写您的邮箱')])
    password = PasswordField(u'密码', validators=[DataRequired(u'密码不能为空')])
    remember_me = BooleanField(u'记住我', default=False)
    submit = SubmitField(u'提交')


class RegisterForm(FlaskForm):
    nickname = StringField(u'昵称', validators=[DataRequired(u'为自己起一个酷酷的昵称吧')])
    email = StringField(u'邮箱', validators=[DataRequired(u'邮箱不能空着哦'), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(u'密码不能空着呀'), Length(6, 18, message=u'密码长度要在6到18位之间的')])
    confirm = PasswordField(u'确认密码', validators=[DataRequired(u'确认密码不能空着哦'),\
                            Length(6, 18, message=u'密码长度要在6到18位之间的'), EqualTo('password', message=u'两次密码好像不一样')])
    submit = SubmitField(u'提交')


class ForgetPasswordForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(u'邮箱不能空着哦'), Email()])
    submit = SubmitField(u'提交')


class ResetPasswordForm(FlaskForm):
    password = StringField(u'新密码', validators=[DataRequired(u'密码不能空着哦')])
    confirm = StringField(u'确认密码', validators=[DataRequired(u'确认密码可不能忘哦'), EqualTo(u'两次密码好像不一样')])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    nickname = StringField(u'昵称', validators=[Length(0, 64)])
    city = StringField(u'城市', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'提交')


class NewArticleFrom(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(u'为这篇精彩的文章起一个标题吧')])
    body = PageDownField(u'内容', validators=[DataRequired(u'文章不能没有内容哦')],\
                         render_kw={'rows': 14, 'placeholder': u'支持markdown，暂不支持上传图片，更多请看写作帮助'})
    submit = SubmitField(u'提交')
