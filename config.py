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
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:security@localhost:3306/blog?charset=utf8mb4'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# mail server,port,username,password of sender
MAIL_SERVER = 'smtp.mxhichina.com'
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'zhancongc@lightblog.site'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Zcc940822'

# whether to use tls and ssl
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# the subject of mail
FLASK_MAIL_SUBJECT_PREFIX = 'Light Blog'

# whether to debug the mail, it is not suggested in product environment
MAIL_DEBUG = True

# articles displayed per page
FLASK_ARTICLE_PER_PAGE = 5

# followers or followed_by displayed per page
FLASK_FOLLOW_PER_PAGE = 20

# comments' number one page show
FLASK_COMMENTS_PER_PAGE = 10
