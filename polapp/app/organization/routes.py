from flask import Blueprint, g, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app import db
from app.search.forms import SearchForm
from app.organization.models import Organization, Event
from app.organization.forms import CreateOrganizationForm, EditOrganizationForm, CreateEventForm, EditEventForm
from datetime import datetime

bp = Blueprint('organization', __name__)

@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()

@bp.route('/organizations')
@login_required
def organizations():
	orgs = current_user.orgs.all()
	create_form = CreateOrganizationForm()
	edit_form = EditOrganizationForm()
	return render_template('organization/organizations.html', 
				orgs=orgs, create_form=create_form, edit_form=edit_form)

@bp.route('/organizations/edit/<id>', methods=['GET','POST'])
@login_required
def _organizations_edit(id):
	orgs = current_user.orgs.all()
	create_form = CreateOrganizationForm()
	edit_form = EditOrganizationForm()

	org = Organization.query.filter_by(id=id).first_or_404()

	if edit_form.validate_on_submit():
		org.name = edit_form.name.data
		org.description = edit_form.descriptionEdit.data
		org.img = edit_form.img.data	
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('organization.organizations'))
	elif request.method == 'GET':	
		edit_form.name.data = org.name
		edit_form.descriptionEdit.data = org.description
		edit_form.img.data = org.img
	return render_template('organization/organizations.html', 
				orgs=orgs, create_form=create_form, edit_form=edit_form)

@bp.route('/organizations/create', methods=['POST'])
@login_required
def _organizations_create():
	orgs = current_user.orgs.all()
	create_form = CreateOrganizationForm()
	edit_form = EditOrganizationForm()

	if create_form.validate_on_submit():
		org = Organization(
			name=create_form.name.data,
			description=create_form.description.data)
		db.session.add(org)
		for main_org in create_form.main_orgs.data:
			org.add_organization(main_org)
		current_user.add_organization(org)
		db.session.commit()
		flash('Your organization has been created')
		return redirect(url_for('organization.organizations'))
	return render_template('organization/organizations.html', 
				orgs=orgs, create_form=create_form, edit_form=edit_form)

@bp.route('/organizations/<id>')
@login_required
def organization(id):
	org = Organization.query.filter_by(id=id).first_or_404()
	edit_form = EditOrganizationForm()

	return render_template('organization/organization.html', 
				org=org, edit_form=edit_form)

@bp.route('/organizations/<id>/edit', methods=['GET', 'POST'])
@login_required
def _organization_edit(id):
	org = Organization.query.filter_by(id=id).first_or_404()
	edit_form = EditOrganizationForm()

	if edit_form.validate_on_submit():
		org.name = edit_form.name.data
		org.description = edit_form.descriptionEdit.data
		org.img = edit_form.img.data	
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('organization.viewOrganization', id=id))
	elif request.method == 'GET':	
		edit_form.name.data = org.name
		edit_form.descriptionEdit.data = org.description
		edit_form.img.data = org.img
	return render_template('organization/organization.html', 
				org=org, edit_form=edit_form)

@bp.route('/events')
@login_required
def events():
	events = current_user.events.all()
	create_form = CreateEventForm()
	edit_form = EditEventForm()
	return render_template('organization/events.html', 
				events=events, create_form=create_form, edit_form=edit_form)

@bp.route('/events/create', methods=['POST'])
@login_required
def _events_create():
	events = current_user.events.all()
	create_form = CreateEventForm()
	edit_form = EditEventForm()

	if create_form.validate_on_submit():
		event = Event(
			name=create_form.name.data,
			description=create_form.description.data,
			start_time=create_form.start_time.data,
			end_time=create_form.end_time.data)
		db.session.add(event)
		for org in create_form.org.data:
			org.add_event(event)
		current_user.add_event(event)
		db.session.commit()
		flash('Your event has been created')
		return redirect(url_for('organization.events'))
	return render_template('organization/events.html', 
				events=events, create_form=create_form, edit_form=edit_form)

@bp.route('/organizations/edit/<id>', methods=['GET','POST'])
@login_required
def _events_edit(id):
	orgs = current_user.orgs.all()
	create_form = CreateOrganizationForm()
	edit_form = EditOrganizationForm()

	org = Organization.query.filter_by(id=id).first_or_404()

	if edit_form.validate_on_submit():
		org.name = edit_form.name.data
		org.description = edit_form.descriptionEdit.data
		org.img = edit_form.img.data	
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('organization.organizations'))
	elif request.method == 'GET':	
		edit_form.name.data = org.name
		edit_form.descriptionEdit.data = org.description
		edit_form.img.data = org.img
	return render_template('organization/organizations.html', 
				orgs=orgs, create_form=create_form, edit_form=edit_form)