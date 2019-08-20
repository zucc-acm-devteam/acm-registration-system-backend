from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

from app.libs.error_code import NotFound
from app.models.user import User
from app.validators.base import BaseForm as Form


class UsernameForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        user = User.get_user_by_username(self.username.data)
        if not user:
            raise NotFound('The user does not exist')


class PasswordForm(Form):
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class LoginForm(UsernameForm, PasswordForm):
    pass


class RegisterForm(PasswordForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])

    def validate_username(self, value):
        user = User.get_user_by_username(self.username.data)
        if user:
            raise NotFound('The user already exist')


class MailForm(Form):
    mail = StringField(validators=[
        DataRequired(message='Mail cannot be empty'),
        Regexp(r'^\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}$', message='Mail is invalid')
    ])


class CodeForm(Form):
    code = StringField(validators=[DataRequired(message='Code cannot be empty')])
