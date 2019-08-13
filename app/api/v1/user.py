from flask import jsonify, g

from app.libs.error_code import CreateSuccess, NotFound, AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import RegisterForm, CodeForm

api = Redprint('user')


@api.route('', methods=['GET'])
@auth.login_required
def get_current_user_api():
    user = g.user
    return jsonify({
        'code': 0,
        'data': {
            'user': user
        }
    })


@api.route('/<string:username>', methods=['GET'])
@auth.login_required
def get_user_api(username):
    user = User.get_user_by_username(username)
    if not user:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'user': user
        }
    })


@api.route('', methods=['POST'])
def create_user_api():
    form = RegisterForm().validate_for_api()
    User.register(form.username.data, form.password.data, form.nickname.data)
    return CreateSuccess('register successful')


@api.route('activation', methods=['POST'])
@auth.login_required
def activate_user_api():
    form = CodeForm().validate_for_api()
    if not User.check_code(g.user.username, form.code.data):
        raise AuthFailed('code is incorrect')
    User.modify(g.user.username, permission=1)
    return Success('activate success')
