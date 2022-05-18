from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user, login_user, logout_user

from app import bcrypt, db, mailing
from app.forms import Register, Login, ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
from app.models import User, Watchlist

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/')
@user_bp.route('/start_trading')
def home():
	# Add all to db
	# file = "app/static/kucoin_cryptos.json"
	# print(file)
	# #
	# with open(file=file, mode='r') as f:
	# 	data = json.load(f)
	# 	for e in data:
	# 		new_crypto = Crypto(ticker=e['symbol'], kucoin_name=e['name'], kucoin_price_name=f"{e['baseCurrency']}{e['quoteCurrency']}")
	# 		db.session.add(new_crypto)
	# 		db.session.commit()
	return render_template('start_trading.html')


@user_bp.route('/trades')
@login_required
def trades():
	trades = current_user.trades
	return render_template('trades.html', trades=trades)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('user_bp.home'))
	registration_form = Register()
	if registration_form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(registration_form.password.data).decode("utf-8")
		user = User(email=registration_form.email.data,
					username=registration_form.username.data,
					password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f"Account for {registration_form.username.data}", "success")
		return redirect(url_for('user_bp.login'))
	# else:
	# 	flash('Sorry, please choose another email/username')
	return render_template('register.html', registration_form=registration_form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('user_bp.home'))
	login_form = Login()
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, login_form.password.data):
			login_user(user, remember=login_form.remember.data)
			redir_page = request.args.get('next')
			return redirect(redir_page) if redir_page else redirect(url_for('main.portfolio'))
		else:
			flash('Login Unsuccessful. Please check your credentials', 'danger')
	return render_template('login.html', login_form=login_form)


@user_bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('user_bp.home'))


@user_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	form = ResetPasswordRequestForm()
	if current_user.is_authenticated:
		return redirect(url_for('user_bp.home'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			mailing.send_reset_email(user)
		flash('An email has been sent', 'success')
		return redirect(url_for('user_bp.login'))
	return render_template('reset.html', title='Reset Password', form=form)


@user_bp.route('/reset_password_request/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('user_bp.home'))
	user = User.verify_reset_password_token(token=token)
	if not user:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_password_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data)
		user.password = hashed_pw
		db.session.commit()
		flash('Password successfully updated')
		return redirect(url_for('main.crypto'))
	return render_template('reset_password.html', form=form)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = ProfileForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data)
		current_user.password = hashed_pw
		db.session.commit()
		flash('Password successfully updated', 'success')
		return redirect(url_for('user_bp.profile'))
	return render_template('profile.html', form=form)


@user_bp.route('/watchlist', methods=['GET', 'Post'])
@login_required
def watchlist():
	watchlist = current_user.watchlist
	return render_template('watchlist.html', watchlist=watchlist)


@user_bp.route('/watchlist/delete/<int:item_id>', methods=['GET'])
@login_required
def delete_from_watchlist(item_id):
	delete_item = Watchlist.query.get(item_id)
	delete_item.delete_from_watchlist()
	flash('Removed from your watchlist', 'info')
	return redirect(url_for('user_bp.watchlist'))


@user_bp.route('/watchlist/add/<int:crypto_id>', methods=['GET'])
@login_required
def add_to_watchlist(crypto_id):
	for item in current_user.watchlist:
		if crypto_id == item.crypto_id:
			flash('Already in your watchlist', 'info')
			return redirect(url_for('user_bp.watchlist'))
	item = Watchlist(user_id=current_user.id, crypto_id=crypto_id)
	db.session.add(item)
	db.session.commit()
	flash('Added to your watchlist', 'info')
	return redirect(url_for('user_bp.watchlist'))
