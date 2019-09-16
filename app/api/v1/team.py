from flask import jsonify, g

from app.libs.error_code import CreateSuccess, Forbidden, Success, NotFound, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.contest import Contest
from app.models.team import Team
from app.models.team_relationship import TeamRelationship
from app.validators.forms import TeamInfoForm, SearchTeamForm

api = Redprint('team')


@api.route('/<int:id_>', methods=['GET'])
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
    contest = Contest.get_by_id(form['contest_id'])
    if contest.status == 0:
        raise Forbidden('Contest is not available')
    if contest.registration_status == 0:
        raise Forbidden('Contest is not open registration')
    for i in TeamRelationship.search(username=g.user.username)['data']:
        if i.team.contest.id == form['contest_id']:
            raise Forbidden('You already have a team')

    team = Team.create_team(form['name'], form['contest_id'], g.user.username, form['password'])
    TeamRelationship.create_team_relationship(g.user.username, team.id)
    return CreateSuccess('Create team success')


@api.route('/<int:id_>', methods=['PUT'])
@auth.login_required
def modify_team_api(id_):
    team = Team.get_by_id(id_)
    if not team:
        raise NotFound()
    contest = team.contest
    if contest.status == 0:
        raise Forbidden('Contest is not available')
    if contest.registration_status == 0:
        raise Forbidden('Contest is not open registration')
    if g.user.permission != -1 and g.user.username != team.create_username:
        raise Forbidden()
    form = TeamInfoForm().validate_for_api().data_
    if g.user.permission != -1 and form['status'] not in [0, 1]:
        raise Forbidden()

    Team.modify(id_, **form)
    return Success('Modify team success')


@api.route('/<int:id_>', methods=['DELETE'])
@auth.login_required
def delete_team_api(id_):
    team = Team.get_by_id(id_)
    if not team:
        raise NotFound()
    contest = team.contest
    if contest.status == 0:
        raise Forbidden('Contest is not available')
    if contest.registration_status == 0:
        raise Forbidden('Contest is not open registration')
    if g.user.permission != -1 and g.user.username != team.create_username:
        raise Forbidden()
    team_relationship = TeamRelationship.search(team_id=team.id)
    if team_relationship['count'] != 1:
        raise Forbidden('There are other members in the team')
    TeamRelationship.delete_team_relationship(team_relationship['data'][0].id)
    Team.delete_team(id_)
    return DeleteSuccess('Delete team success')
