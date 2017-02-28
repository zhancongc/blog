# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# debug program
DEBUG = True
# enable csrf
CSRF_ENABLED = True
# secret key to prevent csrf attack
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

# track modifications is suggested opening
SQLALCHEMY_TRACK_MODIFICATIONS = True
# uri of database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/blog?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# mail server,port,username,password of sender
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 25
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1227753320@qq.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'zaq1234567890okm'

# whether to use tls and ssl
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# the subject of mail
FLASK_MAIL_SUBJECT_PREFIX = 'Light Blog'

# whether to debug the mail, it is not suggested in product environment
MAIL_DEBUG = True

# articles displayed per page
FLASK_ARTICLE_PER_PAGE = 10

# followers or followed_by displayed per page
FLASK_FOLLOW_PER_PAGE = 10

