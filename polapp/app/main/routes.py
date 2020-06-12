from flask import Blueprint, g, render_template, send_file, abort
from flask_login import login_required, current_user
from app import db
from app.search.forms import SearchForm
from datetime import datetime

bp = Blueprint('index', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/download/<file_type>/<file_name>')
@login_required
def download(file_type, file_name=None):
	try:
		if file_type == 'generate' and file_name == 'rapport':
			file = f'./files/DOWNLOAD_THIS.txt'
			return send_file(file, as_attachment=True)
		else:
			file = f'./files/{file_type}/{file_name}'
			return send_file(file, as_attachment=True)
	except FileNotFoundError:
		abort(404)

@bp.route('/404')
def error(e=404):
	return render_template('pages/404.html'), 404

@bp.route('/blank')
def blank():
	return render_template('pages/blank.html')

@bp.route('/utilities/animation')
def animation():
    return render_template('utilities/animation.html')

@bp.route('/utilities/border')
def border():
    return render_template('utilities/border.html')

@bp.route('/utilities/color')
def color():
    return render_template('utilities/color.html')

@bp.route('/utilities/other')
def other():
    return render_template('utilities/other.html')

@bp.route('/elements/buttons')
def buttons():
    return render_template('elements/buttons.html')

@bp.route('/elements/cards')
def cards():
    return render_template('elements/cards.html')

@bp.route('/elements/charts')
def charts():
    return render_template('elements/charts.html')

@bp.route('/elements/tables')
def tables():
    return render_template('elements/tables.html')

