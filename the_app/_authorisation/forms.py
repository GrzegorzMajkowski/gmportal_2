from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed # related to updating profile picture of user

#imports related to user
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('E-mail: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

class RegistrationForm(FlaskForm):
    email = StringField('E-mail: ', validators=[DataRequired(), Email(message='Niewłaściwy format e-mail')])
    username = StringField('Użytkownik: ', validators=[DataRequired()])
    password = PasswordField('Hasło: ', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords must match BUM!')])
    pass_confirm = PasswordField('Potwierdź hasło: ', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

    def check_email(self, field):
        # if User.query.filter_by(email=field.data).first():
        #     raise ValidationError('Your email has been registerd already!')
        pass
    
    def check_username(self, field):
        # if User.query.filter_by(username=field.data).first():
        #     raise ValidationError('Your username has been registerd already!')
        pass

class UpdateUserForm(FlaskForm):
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    username = StringField('Username: ', validators=[DataRequired()])
    picture = FileField('Update Profile Picture: ', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

