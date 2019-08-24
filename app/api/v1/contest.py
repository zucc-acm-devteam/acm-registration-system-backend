from flask import jsonify

from app.libs.error_code import CreateSuccess, Success, NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.contest import Contest
from app.validators.forms import ContestInfoForm, SearchContestForm

api = Redprint('contest')


@api.route('/<int:id_>', methods=['GET'])
@auth.login_required
def get_contest_api(id_):
    contest = Contest.get_by_id(id_)
    if not contest:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'contest': contest
        }
    })


@api.route('/', methods=['GET'])
@auth.login_required
def search_contest_api():
    form = SearchContestForm().validate_for_api().data_
    res = Contest.search(**form)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
@auth.login_required
def create_contest_api():
    form = ContestInfoForm().validate_for_api().data_
    Contest.create_contest(form['name'], form['limit_num'])
    return CreateSuccess('Create contest success')


@api.route('/<int:id_>', methods=['PUT'])
@auth.login_required
def modify_contest_api(id_):
    contest = Contest.get_by_id(id_)
    if not contest:
        raise NotFound()
    form = ContestInfoForm().validate_for_api().data_
    Contest.modify(id_, **form)
    return Success('Modify contest success')
