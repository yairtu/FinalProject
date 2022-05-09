import time
import jwt
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import abort

from app import db, create_app
from datetime import datetime
from app import login_manager
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(20), unique=True, nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	usd = db.Column(db.Float, default=10000.0)
	admin = db.Column(db.Boolean, default=False)
	trades = db.relationship('Trade', backref='user')
	portfolio = db.relationship('Portfolio', backref='user_portfolio')
	watchlist = db.relationship('Watchlist', backref='user_watchlist')

	def get_reset_password_token(self, expires_in=600):
		timeout = time.time() + expires_in
		payload = {
			'reset_password': self.id,
			'exp': timeout
		}

		# Get the secret key from config
		secret_key = create_app().config['SECRET_KEY']

		# Create the token
		token = jwt.encode(payload=payload, key=secret_key, algorithm="HS256")

		# Turn it to string
		s_token = token

		return s_token

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, create_app().config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)


class Crypto(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ticker = db.Column(db.String(20))
	kucoin_name = db.Column(db.String(20))
	kucoin_price_name = db.Column(db.String(20))
	trade = db.relationship('Trade', backref='crypto')
	watchlist = db.relationship('Watchlist', backref='crypto')


# class Stock(db.Model):
# 	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# 	alpaca_id = db.Column(db.String(100))
# 	ticker = db.Column(db.String(20))
# 	name = db.Column(db.String(20))


class Trade(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	trade_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	quantity = db.Column(db.Float, nullable=False)
	current_price = db.Column(db.Float)
	crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	buy = db.Column(db.Boolean, nullable=False)


class Portfolio(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	crypto_id = db.Column(db.Integer)
	ticker = db.Column(db.String(10))
	quantity = db.Column(db.Float, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Watchlist(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'))

	def delete_from_watchlist(self):
		db.session.delete(self)
		db.session.commit()


class SecureModelView(ModelView):
	def is_accessible(self):
		try:
			if current_user.admin:
				return current_user.admin
			else:
				abort(404)
		except AttributeError:
			return abort(403)


class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		try:
			return current_user.admin
		except AttributeError:
			return abort(403)