from flask import Blueprint
from app.api.v1 import user, token, mail


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    token.api.register(bp_v1)
    mail.api.register(bp_v1)
    return bp_v1
