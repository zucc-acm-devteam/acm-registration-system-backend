from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Regexp, ValidationError

from app.libs.error_code import NotFound
from app.models.contest import Contest
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


class UuidForm(Form):
    uuid = StringField(validators=[DataRequired(message='Uuid cannot be empty')])


class LoginForm(UsernameForm, PasswordForm):
    pass


class RegisterForm(PasswordForm, UuidForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

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


class UserInfoForm(Form):
    gender = IntegerField(validators=[DataRequired(message='Gender cannot be empty')])
    college = StringField(validators=[DataRequired(message='College cannot be empty')])
    profession = StringField(validators=[DataRequired(message='Profession cannot be empty')])
    class_ = StringField(validators=[DataRequired(message='Class cannot be empty')])
    phone = StringField(validators=[DataRequired(message='Phone cannot be empty')])
    qq = StringField(validators=[DataRequired(message='QQ cannot be empty')])
    remark = StringField()


class TeamInfoForm(Form):
    name = StringField(validators=[DataRequired(message='Name cannot be empty')])
    contest_id = IntegerField(validators=[DataRequired(message='Contest id cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])

    def validate_contest_id(self, value):
        contest = Contest.get_by_id(self.contest_id.data)
        if not contest:
            raise NotFound('The contest does not exist')


class ContestInfoForm(Form):
    name = StringField(validators=[DataRequired(message='Name cannot be empty')])
    limit_num = IntegerField(validators=[DataRequired(message='Limit number cannot be empty')])
    status = IntegerField()

    def validate_status(self, value):
        if self.status.data != 0 and self.status.data != 1:
            raise ValidationError('Status only can be 0 or 1')


class PageForm(Form):
    page = IntegerField()
    page_size = IntegerField()

    def validate_page(self, value):
        if self.page.data:
            if self.page.data <= 0:
                raise ValidationError('Page must >= 1')
        else:
            self.page.data = 1

    def validate_page_size(self, value):
        if self.page_size.data:
            if self.page_size.data > 100:
                raise ValidationError('Page size must <= 100')
        else:
            self.page_size.data = 20


class SearchUserForm(PageForm):
    nickname = StringField()
    gender = StringField()
    college = StringField()
    profession = StringField()
    class_ = StringField()
    phone = StringField()
    qq = StringField()
    permission = IntegerField()
    remark = StringField()


class SearchContestForm(PageForm):
    name = StringField()
    limit_num = IntegerField()
    status = IntegerField()


class SearchTeamForm(PageForm):
    name = StringField()
    contest_id = IntegerField()
