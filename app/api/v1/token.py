from flask import current_app, jsonify

from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import LoginForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token_api():
    form = LoginForm().validate_for_api()
    identity = User.verify(form.username.data, form.password.data)
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = _generate_auth_token(identity['uid'], expiration)
    return jsonify({
        'code': 0,
        'data': {
            'token': token.decode('ascii')
        }
    }), 201


def _generate_auth_token(uid, expiration):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid
    })
