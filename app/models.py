# -*- coding: utf-8 -*-

from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import Markdown
import bleach


class Follow(db.Model):
    # connect two users by following

    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    # record the users of the light blog

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    city = db.Column(db.UnicodeText(64))
    about_me = db.Column(db.UnicodeText)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    confirmed = db.Column(db.Boolean, default=False)
    followed = db.relationship('Follow',  # ta关注者的人
                               foreign_keys=[Follow.follower_id],  # 外键，可选
                               backref=db.backref('follower', lazy='joined'),  # 连接到关注者，一次加载全部关联实例
                               lazy='dynamic',  # 关系属性返回查询对象，便于增加额外的查询条件
                               cascade='all, delete-orphan')  # 删除该对象之后，顺便销毁指向该记录的实体
    followers = db.relationship('Follow',  # 关注ta的人
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_articles(self):
        return Article.query.join(Follow, Follow.followed_id == Article.author_id).filter(Follow.follower_id == self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return self.confirmed

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.nickname


class Article(db.Model):
    # record the article which created by users

    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), index=True)
    body = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    valid = db.Column(db.Boolean, default=True)

    @staticmethod
    def on_changed_body(target, value, old_value, initiator):
        m = Markdown()
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code','em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'img', 'audio']
        target.body_html = bleach.linkify(bleach.clean(m.convert(value),tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Post %r>' % self.body

db.event.listen(Article.body, 'set', Article.on_changed_body)


class Comment(db.Model):
    # reader's opinions, linked to article

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    commenter = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


class Favorite(db.Model):
    # record someone likes an article

    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    article = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    valid = db.Column(db.Boolean, default=False)


class Read(db.Model):
    # record whom the article read by

    __tablename__ = 'read'
    id = db.Column(db.Integer, primary_key=True)
    reader = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    article = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    timestamp = db.Column(db.DateTime, index=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
