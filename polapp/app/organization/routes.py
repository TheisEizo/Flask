from flask import Blueprint, g, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app import db
from app.search.forms import SearchForm
from app.organization.models import Organization
from app.organization.forms import CreateOrganizationForm, EditOrganizationForm
from datetime import datetime

bp = Blueprint('organization', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()


@bp.route('/organization', methods=['GET', 'POST'])
@login_required
def organizations():
	orgs = current_user.orgs.all()
	create_form = CreateOrganizationForm()

	if create_form.validate_on_submit():
		org = Organization(
			name=create_form.name.data, 
			description=create_form.description.data)
		db.session.add(org)
		current_user.add_organization(org)
		db.session.commit()
		flash('Your organization has been created')
		return redirect(url_for('organization.organizations'))
	
	return render_template('organization/organizations.html', 
				orgs=orgs, create_form=create_form)

@bp.route('/organization/<id>', methods=['GET', 'POST'])
@login_required
def view_organization(id):
	org = Organization.query.filter_by(id=id).first_or_404()
	edit_form = EditOrganizationForm()
	if edit_form.validate_on_submit():
		org.name = edit_form.name.data
		org.description = edit_form.description.data
		org.img = edit_form.img.data	
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('organization.view_organization', id=id))
	elif request.method == 'GET':	
		edit_form.name.data = org.name
		edit_form.description.data = org.description
		edit_form.img.data = org.img
	return render_template('organization/view_organization.html', 
				org=org, edit_form=edit_form)

