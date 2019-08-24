from flask import jsonify, g

from app.libs.error_code import CreateSuccess, Forbidden, Success, NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.team import Team
from app.validators.forms import TeamInfoForm, SearchTeamForm

api = Redprint('team')


@api.route('/<int:id_>', methods=['GET'])
@auth.login_required
def get_team_api(id_):
    team = Team.get_by_id(id_)
    if not team:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'team': team
        }
    })


@api.route('/', methods=['GET'])
@auth.login_required
def search_team_api():
    form = SearchTeamForm().validate_for_api().data_
    res = Team.search(**form)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
@auth.login_required
def create_team_api():
    form = TeamInfoForm().validate_for_api().data_
    Team.create_team(form['name'], form['contest_id'], g.user.username, form['password'])
    return CreateSuccess('Create team success')


@api.route('/<int:id_>', methods=['PUT'])
def modify_team_api(id_):
    team = Team.get_team_by_id(id_)
    if not team:
        raise NotFound()
    if g.user.username != -1 and g.user.username != team.create_username:
        raise Forbidden()

    form = TeamInfoForm().validate_for_api().data_
    Team.modify(id_, **form)
    return Success('Modify team success')
