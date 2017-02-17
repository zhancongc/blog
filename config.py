import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1227753320@qq.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'zaq1234567890okm'
FLASK_MAIL_SUBJECT_PREFIX = 'Pure Blog'
MAIL_DEBUG = True

