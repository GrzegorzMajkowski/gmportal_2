from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired

#imports related to user

class LosowaForm(FlaskForm):
    input_value = StringField('Liczba losowa: ', validators=[DataRequired()])
    submit = SubmitField('Sprawdź odpowiedź...')
