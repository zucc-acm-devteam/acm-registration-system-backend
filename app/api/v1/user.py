from flask import jsonify, g

from app.libs.error_code import CreateSuccess, NotFound, Success, Forbidden
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import RegisterForm
from app import redis as rd

api = Redprint('user')


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


@api.route('/register/<string:uuid>', methods=['POST'])
def register_user_api(uuid):
    _verification(uuid)
    form = RegisterForm().validate_for_api()
    User.register(form.username.data, form.password.data, form.nickname.data)
    return CreateSuccess('register successful')


@api.route('/activation/<string:uuid>', methods=['POST'])
@auth.login_required
def activate_user_api(uuid):
    _verification(uuid)
    User.modify(g.user.username, permission=1)
    return Success('activate success')


def _verification(uuid):
    if not int(rd.hget(uuid, 'success').decode('utf8')):
        raise Forbidden()
    rd.delete(uuid)
