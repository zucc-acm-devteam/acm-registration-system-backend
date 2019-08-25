from flask import Blueprint
from app.api.v1 import user, token, captcha, contest, team, announcement, team_relationship


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    token.api.register(bp_v1)
    captcha.api.register(bp_v1)
    contest.api.register(bp_v1)
    team.api.register(bp_v1)
    announcement.api.register(bp_v1)
    team_relationship.api.register(bp_v1)
    return bp_v1
