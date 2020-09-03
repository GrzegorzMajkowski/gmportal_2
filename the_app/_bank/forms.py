from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Email
from wtforms import ValidationError

class Customer_form(FlaskForm):
    first_name = StringField('Imię',validators=[DataRequired()])
    last_name = StringField('Nazwisko',validators=[DataRequired()])
    email = StringField('e-mail',validators=[Email(message='Niewłaściwy format e-mail!'),DataRequired()])
    address = StringField('Adres',validators=[DataRequired()])
    city = StringField('Miasto',validators=[DataRequired()])
    birth_date = DateField('Data urodzenia', format='%Y-%m-%d',validators=[DataRequired(message='Niewłaściwy format daty!')])
    customer_number = StringField('Nr klienta')
    enrollment_date = DateField('Data utworzenia')
    submit = SubmitField('Zapisz')

class Search_for_customer(FlaskForm):
    name = StringField('Wyszukaj nazwiska zawierające:',validators=[DataRequired()])
    submit = SubmitField('Wyszukaj')

class Go_to_account(FlaskForm):
    account = StringField('Przejdź do rachunku:',validators=[DataRequired()])
    submit = SubmitField('Wykonaj')

class Create_account(FlaskForm):
    account_name = StringField('Podaj nazwę nowego rachunku:',validators=[DataRequired()])
    submit = SubmitField('Utwórz')

class Cash_in_out(FlaskForm):
    quote = StringField('Podaj kwotę transakcji kasowej:',validators=[DataRequired()])
    submit = SubmitField('Wykonaj')


class Money_transfer(FlaskForm):
    target_account_number = StringField('Nr konta docelowego:', validators=[DataRequired()])
    transfer_title = StringField('Tytuł przelewu:', validators=[DataRequired()])
    quote = StringField('Podaj kwotę przelewu:',validators=[DataRequired()])
    submit = SubmitField('Wykonaj')

class Search_form(FlaskForm):
    search_result = StringField('Wpisz wyszukiwany numer :',validators=[DataRequired()])
    submit = SubmitField('Wyszukaj')

