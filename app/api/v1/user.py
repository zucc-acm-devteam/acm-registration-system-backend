from flask import jsonify, g

from app.libs.error_code import CreateSuccess, Success, Forbidden, NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import RegisterForm, UuidForm, UserInfoForm, SearchUserForm
from app import redis as rd

api = Redprint('user')


@api.route('/<string:username>', methods=['GET'])
@auth.login_required
def get_user_api(username):
    user = User.get_by_id(username)
    if not user:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'user': user
        }
    })


@api.route('/', methods=['GET'])
@auth.login_required
def search_user_api():
    form = SearchUserForm().validate_for_api().data_
    res = User.search(**form)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
def register_user_api():
    form = RegisterForm().validate_for_api().data_
    _verification(form['uuid'])
    User.register(form['username'], form['password'])
    return CreateSuccess('register successful')


@api.route('/<string:username>', methods=['PUT'])
@auth.login_required
def modify_user_api(username):
    user = User.get_by_id(username)
    if not user:
        raise NotFound()
    if g.user.profession != -1 and g.user.username != username:
        raise Forbidden()

    form = UserInfoForm().validate_for_api().data_
    User.modify(username, **form)
    return Success('Modify user success')


@api.route('/activation', methods=['POST'])
@auth.login_required
def activate_user_api():
    form = UuidForm().validate_for_api().data_
    _verification(form['uuid'])
    User.modify(g.user.username, permission=1)
    return Success('activate success')


def _verification(uuid):
    if not int(rd.hget(uuid, 'success').decode('utf8')):
        raise Forbidden()
    rd.delete(uuid)
