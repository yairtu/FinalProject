import flask
from flask import Blueprint

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.errorhandler(404)
def error_404(error):
	return flask.render_template('404_error.html'), 404


@error_handlers.errorhandler(429)
def error_429(error):
	return flask.render_template('404_error.html'), 429