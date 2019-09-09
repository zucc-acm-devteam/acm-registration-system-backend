import hashlib
import time

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.config.secure import WHITELIST_UA
from app.libs.error_code import AuthFailed, Forbidden, NotFound
from app.libs.scope import is_in_scope
from app.models.user import User

auth = HTTPBasicAuth()


def md5(raw):
    return hashlib.md5(raw.encode('utf8')).hexdigest()


@auth.verify_password
def verify_token(token, secret):
    ua = request.headers.get('User-Agent', '')
    if ua != WHITELIST_UA:
        timestamp = int(request.headers.get('Timestamp', 0))
        if abs(timestamp - int(time.time())) > 100:
            raise AuthFailed()

        my_secret = md5(token + str(timestamp))
        if my_secret != secret:
            raise AuthFailed()

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    user = User.get_by_id(uid)
    if not user:
        raise NotFound()
    allow = is_in_scope(user.scope, request.endpoint)
    if not allow:
        raise Forbidden()
    g.user = user
    return True
