from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, FloatField, EmailField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, ValidationError, Email
from app.models import User


class Search(FlaskForm):
	search = StringField("Search for ticker")
	submit = SubmitField('Search')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')


class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')


class Login(FlaskForm):
	username = StringField("Username",
						   validators=[InputRequired(message="Please enter your username"),
									   Length(min=3, max=12)])
	password = PasswordField("Password",
							 validators=[InputRequired(message="Please enter your password"),
										 Length(min=4, max=14)])
	remember = BooleanField("Remember me")
	login = SubmitField("Login")


class Register(FlaskForm):
	email = EmailField("Email")
	username = StringField("Username",
						   validators=[InputRequired(message="Please choose a username"),
									   Length(min=3, max=12)])
	password = PasswordField("Password",
							 validators=[DataRequired(Length(min=4, max=14))])
	confirm_password = PasswordField("Confirm Password",
									 validators=[DataRequired(Length(min=4, max=14)), EqualTo("password")])
	register = SubmitField("Sign up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username is taken. Please choose a different one.")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That email is taken. Please choose a different one.")


class BuyForm(FlaskForm):
	amount = FloatField("Amount")
	submit = SubmitField("Buy")


class SellForm(FlaskForm):
	amount = FloatField("Amount")
	submit = SubmitField("Sell")


class ProfileForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(Length(min=4, max=14))])
	submit = SubmitField("Change Password")


class WatchlistForm(FlaskForm):
	submit = SubmitField('Add to Watchlist', render_kw={"placeholder": "test"})
	remove = SubmitField('Remove from Watchlist')
