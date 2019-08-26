from flask import jsonify, g

from app.libs.error_code import CreateSuccess, NotFound, DeleteSuccess, Forbidden
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.team import Team
from app.models.team_relationship import TeamRelationship
from app.validators.forms import SearchTeamRelationshipForm, TeamRelationshipForm

api = Redprint('team_relationship')


@api.route('/', methods=['GET'])
@auth.login_required
def search_team_relationship_api():
    form = SearchTeamRelationshipForm().validate_for_api().data_
    res = TeamRelationship.search(**form)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
@auth.login_required
def create_team_relationship_api():
    form = TeamRelationshipForm().validate_for_api().data_
    team = Team.get_by_id(form['team_id'])
    if team.contest.status == 0:
        raise Forbidden('Contest is not available')
    for i in TeamRelationship.search(username=g.user.username):
        if i.team_id == form['team_id']:
            raise Forbidden('You already have a team')
    if not team.check_password(form['password']):
        raise Forbidden('Password wrong')

    TeamRelationship.create_team_relationship(g.user.username, form['team_id'])
    return CreateSuccess('Create team relationship success')


@api.route('/<int:id_>', methods=['DELETE'])
@auth.login_required
def delete_team_relationship_api(id_):
    team_relationship = TeamRelationship.get_by_id(id_)
    if not team_relationship:
        raise NotFound()
    contest = TeamRelationship.get_by_id(id_).team.contest
    if contest.status == 0:
        raise Forbidden('Contest is not available')
    if team_relationship.username != g.user.username:
        raise Forbidden()
    if team_relationship.team.create_username == team_relationship.username:
        raise Forbidden('Can not quit the team you created')

    TeamRelationship.delete_team_relationship(id_)
    return DeleteSuccess('Delete team relationship success')
