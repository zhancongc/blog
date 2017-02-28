# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

moment = Moment(app)

mail = Mail(app)

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/auth/login'

pagedown = PageDown(app)

from app import models, views
from app.views import auth, art, user, foll

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(art, url_prefix='/article')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(foll)
