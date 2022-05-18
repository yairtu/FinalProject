from flask import render_template, request, Blueprint, flash, redirect, url_for
from app import htmx
from flask_login import current_user, login_required

from app import db
from app.forms import BuyForm, SellForm, WatchlistForm
from app.models import Crypto, Trade, Portfolio
from app.api import get_news, get_price, get_trending
import git

main = Blueprint('main', __name__)

@main.route('/git_update', methods=['POST'])
def git_update():
	if current_user.admin:
		repo = git.Repo('./FinalProject')
		origin = repo.remotes.origin
		repo.create_head('main',
						 origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
		origin.pull()
		return '', 200


@main.route('/crypto', methods=['GET', 'POST'])
def crypto():
	form = WatchlistForm()
	if form.validate_on_submit():
		return
	page = request.args.get('page', default=1, type=int)
	all_tickers = Crypto.query.paginate(page=page, per_page=10, error_out=False)

	if htmx:
		all_tickers = Crypto.query.paginate(page=page, per_page=10, error_out=False)
		return render_template('partials/current_price.html', tickers=all_tickers)
	return render_template('index.html', tickers=all_tickers, form=form)


# @main.route('/stock', methods=['GET', 'POST'])
# def stock():
# 	page = request.args.get('page', default=1, type=int)
# 	all_stocks = Stock.query.paginate(per_page=10, error_out=False)
# 	return render_template('stock.html', stocks=all_stocks)


@main.route('/search', methods=['GET', 'POST'])
def searched():
	q = request.args.get('q').lower()
	all_crypto = Crypto.query.all()
	searched = []
	for crypto in all_crypto:
		if q in crypto.ticker.lower():
			searched.append(crypto)
	return render_template('searched.html', crypto=searched)


@main.route('/trending')
def trending():
	trending_dict = get_trending()
	return render_template('trending.html', trending=trending_dict)


@main.route('/buy/<ticker>', methods=['GET', 'POST'])
@login_required
def buy(ticker):
	form = BuyForm()
	crypto = Crypto.query.filter_by(ticker=ticker).first()
	if htmx:
		return render_template('partials/price.html', ticker=ticker)
	current_usd = current_user.usd
	price = float(get_price(crypto.ticker))
	holding_amount = current_holding_amount(crypto.id)
	holding_value = value(price=price, quantity=holding_amount)
	max_buy_amount = current_usd / price
	if form.validate_on_submit():
		if max_buy_amount < form.amount.data:
			flash(f"You cannot exceed the maximum buy amount", "danger")
			return redirect(url_for('main.buy', ticker=ticker))
		else:
			trade = Trade(quantity=form.amount.data, current_price=price, crypto=crypto, user=current_user, buy=True)
			user_portfolio = current_user.portfolio
			for item in user_portfolio:
				if int(item.crypto_id) == crypto.id:
					item.quantity += trade.quantity
					db.session.add(trade)
					db.session.commit()
					return redirect(url_for('main.portfolio'))
			portfolio = Portfolio(crypto_id=crypto.id, ticker=crypto.ticker,
								  quantity=form.amount.data, user_portfolio=current_user)
			db.session.add(portfolio)
			db.session.commit()
			current_user.usd = current_user.usd - (price * form.amount.data)
			db.session.add(trade)
			db.session.commit()
			return redirect(url_for('main.portfolio'))
	context = {
		'crypto': crypto,
		'value': holding_value,
		'holding': holding_amount,
		'max_buy_amount': max_buy_amount,
		'form': form,
		'price': price,
	}
	return render_template('buy.html', **context)


@main.route('/sell/<ticker>', methods=['GET', 'POST'])
@login_required
def sell(ticker):
	if htmx:
		return render_template('partials/price.html', ticker=ticker)
	form = SellForm()
	crypto = Crypto.query.filter_by(ticker=ticker).first()
	price = get_price(crypto.ticker)
	holding_amount = current_holding_amount(crypto.id)
	holding_value = value(price=float(price), quantity=holding_amount)
	if form.validate_on_submit():
		if holding_amount < form.amount.data:
			flash(f"Your sell amount cannot exceed your holding quantity", "danger")
			return redirect(url_for('main.sell', ticker=ticker))
		else:
			trade = Trade(quantity=form.amount.data, current_price=price, crypto=crypto, user=current_user, buy=False)
			current_user.usd += float(price) * form.amount.data
			user_portfolio = current_user.portfolio
			for item in user_portfolio:
				if int(item.crypto_id) == crypto.id:
					item.quantity -= trade.quantity
					if item.quantity == 0:
						db.session.delete(item)
						db.session.commit()
			db.session.add(trade)
			db.session.commit()
			return redirect(url_for('main.portfolio'))
	context = {
		'crypto': crypto,
		'value': holding_value,
		'holding': holding_amount,
		'form': form,
		'price': price,
	}
	return render_template('sell.html', **context)


@main.route('/news')
def news():
	news = get_news()
	return render_template('news.html', news=news)


@main.route('/portfolio')
@login_required
def portfolio():
	portfolio_data = []
	portfolio = current_user.portfolio
	total_holding_value = 0
	for item in portfolio:
		crypto = Crypto.query.filter_by(id=item.crypto_id).first()
		price = get_price(crypto.ticker)
		current_holding_value = value(price=float(price), quantity=item.quantity)
		portfolio_data.append(
			{'ticker': crypto.ticker,
			 'price': price,
			 'holding_amount': item.quantity,
			 'current_holding_value': current_holding_value
			 }
		)
		total_holding_value += current_holding_value
	percent_change = (total_holding_value + current_user.usd - 10000) / 100
	context = {
		'portfolio': portfolio_data,
		'percent_change': percent_change
	}
	if htmx:
		return render_template('partials/portfolio_price.html', **context)
	return render_template('portfolio.html', **context)


def current_holding_amount(crypto_id):
	user_portfolio = current_user.portfolio
	for item in user_portfolio:
		if int(item.crypto_id) == crypto_id:
			return item.quantity
	return 0


def value(price: float, quantity: float):
	return price * quantity
