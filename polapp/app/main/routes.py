from flask import Blueprint, g, render_template, send_file, abort, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.search.forms import SearchForm
from app.auth.models import Notification
from datetime import datetime

bp = Blueprint('main', __name__)

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

@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@bp.route('/blank')
def blank():
	return render_template('pages/blank.html')

@bp.route('/utilities/animation')
def animation():
    return render_template('pages/animation.html')

@bp.route('/utilities/border')
def border():
    return render_template('pages/border.html')

@bp.route('/utilities/color')
def color():
    return render_template('pages/color.html')

@bp.route('/utilities/other')
def other():
    return render_template('pages/other.html')

@bp.route('/elements/buttons')
def buttons():
    return render_template('pages/buttons.html')

@bp.route('/elements/cards')
def cards():
    return render_template('pages/cards.html')

@bp.route('/elements/charts')
def charts():
    return render_template('pages/charts.html')

@bp.route('/elements/tables')
def tables():
    return render_template('pages/tables.html')

