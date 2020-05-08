from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class LoginForm(FlaskForm):
    searchtext = StringField('What to search?')
    submit = SubmitField('Search')
