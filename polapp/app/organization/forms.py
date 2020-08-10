from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, SelectField, DateField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
#from wtforms.ext.dateutil.fields import DateTimeField
#from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired, Required
from flask_login import current_user

def orgs():
    return current_user.orgs

class CreateOrganizationForm(FlaskForm):
	name = StringField('Organizaton name', 
		validators=[DataRequired()])
	description = TextAreaField('Description')

	main_orgs = QuerySelectMultipleField('Main Organization', 
			query_factory=orgs, allow_blank=False, 
        		get_label='name', get_pk=lambda x: x.id,
        		blank_text=u'Select a main organization...')

	submit = SubmitField('Submit')

class CreateEventForm(FlaskForm):
	name = StringField('Organizaton name', 
		validators=[DataRequired()])
	description = TextAreaField('Description')

	org = QuerySelectMultipleField('Organization', 
			query_factory=orgs, allow_blank=False, 
        		get_label='name', get_pk=lambda x: x.id,
        		blank_text=u'Select a organization...')

	start_time = DateField('Start', format='%m/%d/%y', validators=[Required()])
	end_time = DateField('End', format='%m/%d/%y', validators=[Required()])

	submit = SubmitField('Submit')

class EditOrganizationForm(FlaskForm):
	name = StringField('Organizaton name', 
		validators=[DataRequired()])
	descriptionEdit = TextAreaField('Description')
	img = StringField('Organizaton image link')
	submitEdit = SubmitField('Submit')

class EditEventForm(FlaskForm):
	name = StringField('Organizaton name', 
		validators=[DataRequired()])
	descriptionEdit = TextAreaField('Description')
	img = StringField('Organizaton image link')

	start_time = DateTimeField('Start', id='datepick2', validators=[Required()])
	end_time = DateTimeField('End', id='datepick3', validators=[Required()])

	submitEdit = SubmitField('Submit')