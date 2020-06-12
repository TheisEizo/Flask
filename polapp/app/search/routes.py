from flask import Blueprint, render_template, url_for, g, request, current_app, redirect
from flask_login import login_required, current_user

from app import db
from app.auth.models import User
from app.search.funcs import search_users
from app.search.forms import SearchForm

from datetime import datetime

bp = Blueprint('search', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    
    users, total = search_users()

    next_url = url_for('search.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('search.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', users=users,
                           next_url=next_url, prev_url=prev_url)
