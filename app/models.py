# coding = utf-8

from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach


class User(UserMixin, db.Model):
    '''user, owner of the pure blog'''

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    city = db.Column(db.UnicodeText(64))
    about_me = db.Column(db.UnicodeText)
    password_hash = db.Column(db.String(128))
    Articles = db.RelationshipProperty('Article', backref='author', lazy=True)
    confirmed = db.Column(db.Boolean, default=False)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

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
        self.confirm =True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.nickname


class Article(db.Model):
    '''article, created by users'''

    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), index=True)
    body = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow )
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def on_changed_body(target, value, old_value, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code','em', 'i',
                        'li','ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Post %r>' % self.body


class Comment(db.Model):
    '''comment, linked to article, reader's opinions'''

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    commenter = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.event.listen(Article.body, 'set', Article.on_changed_body)
