from flask import render_template
from flask_mail import Mail, Message
from app import app, mail
from threading import Thread

from flask import current_app

def send_async_email(msg, app):  
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(msg, app)).start()

def send_password_reset_email(user):
    token = user.get_token('reset_password')
    send_email('[SB ADMIN] Reset Your Password',
	       sender=app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('messages/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('messages/reset_password.html',
                                         user=user, token=token))

def send_validation_email(user):
    token = user.get_token('validate_email')
    send_email('[SB ADMIN] Validate Your Email',
	       sender=app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=render_template('messages/validate_email.txt',
                                         user=user, token=token),
               html_body=render_template('messages/validate_email.html',
                                         user=user, token=token))
