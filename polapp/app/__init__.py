import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app(configfile=None):
	app.config.from_object('config.DefaultConfig')
	Bootstrap(app)
																																									
	from .templates import elements
	app.register_blueprint(elements.bp)

	from .templates import utilities
	app.register_blueprint(utilities.bp)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import index
	app.register_blueprint(index.bp)
	app.add_url_rule('/', endpoint='index')

	app.register_error_handler(404, index.error)
	
	db.init_app(app)
	
	login.init_app(app)
	login.login_view = 'login'
	
	migrate.init_app(app, db)

	mail.init_app(app)
																																			
	return app

from app import auth



