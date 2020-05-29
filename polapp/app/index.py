from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, abort,
)
from werkzeug.exceptions import abort

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/download/<file_type>/<file_name>')
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
	#return send_from_directory('failes', )

@bp.route('/404')
def error(e=404):
    return render_template('pages/404.html'), 404

@bp.route('/blank')
def blank():
    return render_template('pages/blank.html')
