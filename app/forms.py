from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('username', [Required()])
    password = PasswordField('password', [Required()])
    cookie = BooleanField('remember')
