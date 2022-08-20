from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    trigramme = StringField('Trigramme', validators=[DataRequired()])
    submit = SubmitField('Se connecter')