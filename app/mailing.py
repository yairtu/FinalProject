from flask import url_for
from flask_mail import Message
from app import mail
from app.forms import ResetPasswordForm


def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)


def send_reset_email(user):
	token = user.get_reset_password_token()
	form = ResetPasswordForm()
	msg = Message('Password Reset Request',
				  sender='noreply@cryptosimulator.com',
				  recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('user_bp.reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)
