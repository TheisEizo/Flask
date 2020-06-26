from flask import Blueprint, g
from flask_login import current_user
from app import db
from app.search.forms import SearchForm
from datetime import datetime

bp = Blueprint('blank', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()
