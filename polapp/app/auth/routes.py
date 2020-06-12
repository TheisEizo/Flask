from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app

from flask_login import login_user, logout_user, current_user, login_required

from app import db, login
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app.search.forms import SearchForm
from app.messages.funcs import send_password_reset_email, send_validation_email

from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.email_validated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        if user.email_validated: 
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Your Email has not been validated [LINK TO RESEND VALIDATION]', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first_or_404()
        send_validation_email(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('auth/profile.html', user=user, title='Edit Profile',
                           form=form)

@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html',
                           title='Forgot Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token('reset_password', token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', 
			title='Reset Password', form=form)

@bp.route('/user/<username>/validate_email')
def user_validate_email(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user.email_validated:
		flash('Your email already is validated')
	else:
		flash('Your email validation has been sent')
		send_validation_email(user)
	return redirect(url_for('auth.login'))

@bp.route('/validate_email/<token>')
def validate_email(token):
    user = User.verify_token('validate_email', token)
    if not user:
        flash('Your email has NOT been validated. Try again [LINK TO VALIDATION]', 'danger')
        return redirect(url_for('auth.login'))
    if user.email_validated:
        flash('Your email has ALREADY been validated')
        return redirect(url_for('auth.login'))
    user.email_validated = True
    db.session.commit()
    form = ResetPasswordForm()
    flash('Your email has been validated')
    return redirect(url_for('auth.login'))
