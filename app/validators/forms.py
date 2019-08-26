from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Regexp, ValidationError
from app.models.contest import Contest
from app.models.team import Team
from app.models.user import User
from app.validators.base import BaseForm as Form


class UsernameForm(Form):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        user = User.get_by_id(self.username.data)
        if not user:
            raise ValidationError('The user does not exist')


class PasswordForm(Form):
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])


class UuidForm(Form):
    uuid = StringField(validators=[DataRequired(message='Uuid cannot be empty')])


class LoginForm(UsernameForm, PasswordForm):
    pass


class RegisterForm(PasswordForm, UuidForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        if User.get_by_id(self.username.data):
            raise ValidationError('The user already exist')


class MailForm(Form):
    mail = StringField(validators=[
        DataRequired(message='Mail cannot be empty'),
        Regexp(r'^\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}$', message='Mail is invalid')
    ])


class TeamIdForm(Form):
    team_id = IntegerField(validators=[DataRequired(message='Team id cannot be empty')])

    def validate_team_id(self, value):
        if not Team.get_by_id(self.team_id.data):
            raise ValidationError('The team does not exist')


class ContestIdForm(Form):
    contest_id = IntegerField(validators=[DataRequired(message='Contest id cannot be empty')])

    def validate_contest_id(self, value):
        if not Contest.get_by_id(self.contest_id.data):
            raise ValidationError('The contest does not exist')


class CodeForm(Form):
    code = StringField(validators=[DataRequired(message='Code cannot be empty')])


class UserInfoForm(Form):
    nickname = StringField(validators=[DataRequired(message='Nickname cannot be empty')])
    gender = IntegerField(validators=[DataRequired(message='Gender cannot be empty')])
    college = StringField(validators=[DataRequired(message='College cannot be empty')])
    profession = StringField(validators=[DataRequired(message='Profession cannot be empty')])
    class_ = StringField(validators=[DataRequired(message='Class cannot be empty')])
    phone = StringField(validators=[DataRequired(message='Phone cannot be empty')])
    qq = StringField(validators=[DataRequired(message='QQ cannot be empty')])
    remark = StringField()


class TeamInfoForm(ContestIdForm):
    name = StringField(validators=[DataRequired(message='Name cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])
    status = IntegerField()

    def validate_status(self, value):
        if self.status.data not in range(4):
            raise ValidationError('Status only can be 0 to 3')


class ContestInfoForm(Form):
    name = StringField(validators=[DataRequired(message='Name cannot be empty')])
    limit = IntegerField(validators=[DataRequired(message='Limit number cannot be empty')])
    status = IntegerField()

    def validate_status(self, value):
        if self.status.data != 0 and self.status.data != 1:
            raise ValidationError('Status only can be 0 or 1')


class AnnouncementInfoForm(Form):
    contest_id = IntegerField()
    type = IntegerField(validators=[DataRequired(message='Type cannot be empty')])
    content = StringField(validators=[DataRequired(message='Content cannot be empty')])

    def validate_contest_id(self, value):
        if self.contest_id.data:
            if not Contest.get_by_id(self.contest_id.data):
                raise ValidationError('The contest does not exist')


class TeamRelationshipForm(TeamIdForm):
    pass


class PageForm(Form):
    page = IntegerField()
    page_size = IntegerField()

    def validate_page(self, value):
        if self.page.data:
            if int(self.page.data) <= 0:
                raise ValidationError('Page must >= 1')
        else:
            self.page.data = 1

    def validate_page_size(self, value):
        if self.page_size.data:
            if int(self.page_size.data) > 100:
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
    remark = StringField()
    permission = IntegerField()


class SearchContestForm(PageForm):
    name = StringField()
    limit_num = IntegerField()
    status = IntegerField()


class SearchTeamForm(PageForm):
    name = StringField()
    contest_id = IntegerField()
    create_username = StringField()


class SearchAnnouncementForm(PageForm):
    contest_id = IntegerField()
    type = IntegerField()
    content = StringField()


class SearchTeamRelationshipForm(Form):
    username = StringField()
    team_id = IntegerField()
