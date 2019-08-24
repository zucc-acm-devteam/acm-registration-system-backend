from flask import jsonify, g

from app.libs.error_code import CreateSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.contest import Contest
from app.validators.forms import ContestInfoForm

api = Redprint('contest')


@api.route('<int:id_>', methods=['GET'])
@auth.login_required
def get_contest_api(id_):
    contest = Contest.get_contest_by_id(id_)
    return jsonify({
        'code': 0,
        'data': {
            'contest': contest
        }
    })


@api.route('/', methods=['GET'])
@auth.login_required
def search_contest_api():
    pass


@api.route('/', methods=['POST'])
@auth.login_required
def create_contest_api():
    form = ContestInfoForm().validate_for_api()
    Contest.create_contest(form['name'], form['limit_num'], form['status'])
    return CreateSuccess('Create contest success')
