# coding = utf-8

from flask_mail import Message
from flask import render_template
from threading import Thread
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(receiver, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,\
                  sender=app.config['MAIL_USERNAME'], recipients=[receiver])
    msg.body = render_template(template + '.txt', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
