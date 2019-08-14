from flask import current_app, jsonify, g

from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import LoginForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

api = Redprint('token')


@api.route('', methods=['GET'])
@auth.login_required
def get_token_info_api():
    user = g.user
    return jsonify({
        'code': 0,
        'data': {
            'user': user
        }
    })


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


@api.route('', methods=['PUT'])
@auth.login_required
def update_token_api():
    identity = {'uid': g.user.username}
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = _generate_auth_token(identity['uid'], expiration)
    return jsonify({
        'code': 0,
        'data': {
            'token': token.decode('ascii')
        }
    }), 201


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_token_api():
    return DeleteSuccess()


def _generate_auth_token(uid, expiration):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid
    })
