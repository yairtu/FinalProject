from flask import Flask
import flask_migrate
import flask_sqlalchemy
from flask_admin import Admin
from flask_htmx import HTMX
from flask_mail import Mail
from app.config import Config

from flask_bcrypt import Bcrypt
from pycoingecko import CoinGeckoAPI
from flask_login import LoginManager

cg = CoinGeckoAPI()
mail = Mail()
htmx = HTMX()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user_bp.login'
login_manager.login_message_category = 'info'
db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()


def create_app():
	flask_app = Flask(__name__)
	flask_app.config.from_object(Config)

	db.init_app(flask_app)
	migrate.init_app(flask_app, db, render_as_batch=True)
	bcrypt.init_app(flask_app)
	login_manager.init_app(flask_app)
	htmx.init_app(flask_app)
	mail.init_app(flask_app)
	admin = Admin(flask_app)

	# from app import routes, error_handlers, models
	from app.api import get_price
	from app.models import SecureModelView, User, Portfolio, Crypto, Trade

	from app.main.routes import main
	from app.user.routes import user_bp
	from app.error_handlers.routes import error_handlers
	flask_app.register_blueprint(main)
	flask_app.register_blueprint(user_bp)
	flask_app.register_blueprint(error_handlers)

	admin.add_view(SecureModelView(User, db.session, name="admin_user_view"))
	admin.add_view(SecureModelView(Portfolio, db.session))
	admin.add_view(SecureModelView(Crypto, db.session))
	admin.add_view(SecureModelView(Trade, db.session))

	flask_app.jinja_env.globals.update(get_price=get_price)

	return flask_app
