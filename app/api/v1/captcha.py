import base64
import random
from uuid import uuid4
from io import BytesIO

from flask import jsonify

from app.libs.error_code import Success
from app.libs.mail import send_verification_mail
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import VerificationMailForm
from captcha.image import ImageCaptcha
from app import redis as rd

api = Redprint('captcha')


@api.route('/image', methods=['GET'])
@auth.login_required
def get_image_captcha_api():
    uuid = 'I' + _generate_uuid()
    code = _generate_code()
    rd.set(uuid, code)
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


@api.route('/mail', methods=['GET'])
@auth.login_required
def get_mail_captcha_api():
    form = VerificationMailForm().validate_for_api()
    uuid = 'M' + _generate_uuid()
    code = _generate_code()
    rd.set(uuid, code)
    send_verification_mail(form.email.data, code)
    return jsonify({
        'code': 0,
        'data': {
            'uuid': uuid
        }
    })


def _generate_code():
    return str(random.randint(100000, 999999))


def _generate_uuid():
    return str(uuid4())


def _image_to_base64(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str
