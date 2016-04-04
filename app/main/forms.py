from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class WebsiteForm(Form):
    website = StringField('Enter Website to Scrape', validators=[DataRequired()])
    submit = SubmitField('Scrape')

