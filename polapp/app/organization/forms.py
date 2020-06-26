from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CreateOrganizationForm(FlaskForm):
	name = StringField('Organizaton name', validators=[DataRequired()])
	description = TextAreaField('About me')
	submit = SubmitField('Submit')

class EditOrganizationForm(FlaskForm):
	name = StringField('Organizaton name', validators=[DataRequired()])
	description = TextAreaField('About me')
	img = StringField('Organizaton image link')
	submit = SubmitField('Submit')
