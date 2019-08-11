from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden, NotFound
from app.libs.scope import is_in_scope
from app.models.user import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, _):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    user = User.get_user_by_username(uid)
    if not user:
        raise NotFound()
    allow = is_in_scope(user.scope, request.endpoint)
    if not allow:
        raise Forbidden()
    g.user = user
    return True
