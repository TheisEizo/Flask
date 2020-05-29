from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('utilities', __name__)

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


