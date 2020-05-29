from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('elements', __name__)

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


