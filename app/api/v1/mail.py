import random

from flask import g

from app.libs.error_code import Success
from app.libs.mail import send_verification_mail
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.mail import Mail
from app.validators.forms import VerificationMailForm

api = Redprint('mail')


@api.route('/verification', methods=['POST'])
@auth.login_required
def send_verification_mail_api():
    form = VerificationMailForm().validate_for_api()
    code = random.randint(100000, 999999)
    Mail.create_log(g.user.username, form.email.data, code)
    send_verification_mail(form.email.data, code)
    return Success('send verification email successful')
