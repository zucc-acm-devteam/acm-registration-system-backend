from wtforms import StringField
from wtforms.validators import DataRequired

from app.libs.error_code import NotFound
from app.models.user import User
from app.validators.base import BaseForm as Form


class PasswordForm(Form):
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class LoginForm(PasswordForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        user = User.get_user_by_username(self.username.data)
        if not user:
            raise NotFound('The user does not exist')


class RegisterForm(PasswordForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])

    def validate_username(self, value):
        user = User.get_user_by_username(self.username.data)
        if user:
            raise NotFound('The user already exist')
