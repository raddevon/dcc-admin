from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, PasswordField, \
    SubmitField, validators, ValidationError
from models import User


class SignupForm(Form):
    email = TextField(
        'Email', [validators.Required('Please enter your email address.'), validators.Email('Enter a valid email address.')])
    password = PasswordField(
        'Password', [validators.Required('Please enter a password.')])
    submit = SubmitField('Create user')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append(
                'That email is already in use.')
            return False
        else:
            return True


class LoginForm(Form):
    email = TextField(
        'Email', [validators.Required('Email address is required to log in.'), validators.Email('Enter a valid email address.')])
    password = PasswordField(
        'Password', [validators.Required('You must enter your password to log in.')])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append('Invalid email or password')
            return False
