import base64
import random
from uuid import uuid4
from io import BytesIO

from flask import jsonify

from app.libs.error_code import Forbidden, Success, ParameterException
from app.libs.mail import send_verification_mail
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import MailForm, CodeForm
from captcha.image import ImageCaptcha
from app import redis as rd

api = Redprint('captcha')


@api.route('/image', methods=['GET'])
def get_image_captcha_api():
    uuid = 'I-' + _generate_uuid()
    code = _generate_code()
    rd.hmset(uuid, {
        'code': code,
        'success': 0,
    })
    rd.expire(uuid, 300)
    img = ImageCaptcha()
    image = img.generate_image(code)
    base64_str = _image_to_base64(image)
    return jsonify({
        'code': 0,
        'data': {
            'image': base64_str,
            'uuid': uuid
        }
    })


@api.route('/image/<string:uuid>', methods=['POST'])
def check_image_captcha_api(uuid):
    form = CodeForm().validate_for_api()
    if uuid[0] != 'I':
        raise ParameterException()
    _check_code(uuid, form.code.data)
    return Success()


@api.route('/mail', methods=['GET'])
@auth.login_required
def get_mail_captcha_api():
    form = MailForm().validate_for_api()
    uuid = 'M-' + _generate_uuid()
    code = _generate_code()
    rd.hmset(uuid, {
        'code': code,
        'success': 0,
    })
    rd.expire(uuid, 3600)
    send_verification_mail(form.mail.data, code)
    return jsonify({
        'code': 0,
        'data': {
            'uuid': uuid
        }
    })


@api.route('/mail/<string:uuid>', methods=['POST'])
def check_mail_captcha_api(uuid):
    form = CodeForm().validate_for_api()
    if uuid[0] != 'M':
        raise ParameterException()
    _check_code(uuid, form.code.data)
    return Success()


def _generate_code():
    return str(random.randint(100000, 999999))


def _generate_uuid():
    return str(uuid4())


def _image_to_base64(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode("utf8")


def _check_code(uuid, code):
    if rd.hget(uuid, 'code').decode('utf8') != code:
        raise Forbidden('wrong captcha')
    rd.hmset(uuid, {
        'success': 1,
    })
    rd.expire(uuid, 60)
