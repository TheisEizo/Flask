import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment

from elasticsearch import Elasticsearch

app = Flask(__name__)
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
mail = Mail()
moment = Moment()

def create_app(configfile=None):
	app.config.from_object('config.DefaultConfig')
	Bootstrap(app)

	from .main import routes
	app.register_blueprint(routes.bp)
	app.add_url_rule('/', endpoint='index')
	app.register_error_handler(404, routes.error)

	from .auth import routes
	app.register_blueprint(routes.bp)

	from .search import routes
	app.register_blueprint(routes.bp)

	from .messages import routes
	app.register_blueprint(routes.bp)
	
	from .organization import routes
	app.register_blueprint(routes.bp)

	db.init_app(app)
	
	login.init_app(app)
	login.login_view = 'login'
	
	migrate.init_app(app, db)

	mail.init_app(app)

	moment.init_app(app)	

	app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
	if not app.elasticsearch.ping():
		app.elasticsearch = None
		
	return app

from app import auth



