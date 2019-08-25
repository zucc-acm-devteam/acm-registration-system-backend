from flask import jsonify

from app.libs.error_code import CreateSuccess, Success, NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.announcement import Announcement
from app.validators.forms import SearchAnnouncementForm, AnnouncementInfoForm

api = Redprint('announcement')


@api.route('/<int:id_>', methods=['GET'])
@auth.login_required
def get_announcement_api(id_):
    announcement = Announcement.get_by_id(id_)
    if not announcement:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'announcement': announcement
        }
    })


@api.route('/', methods=['GET'])
@auth.login_required
def search_announcement_api():
    form = SearchAnnouncementForm().validate_for_api().data_
    res = Announcement.search(**form)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
@auth.login_required
def create_announcement_api():
    form = AnnouncementInfoForm().validate_for_api().data_
    Announcement.create_announcement(form['contest_id'], form['type'], form['content'])
    return CreateSuccess('Create announcement success')


@api.route('/<int:id_>', methods=['PUT'])
def modify_announcement_api(id_):
    announcement = Announcement.get_by_id(id_)
    if not announcement:
        raise NotFound()

    form = AnnouncementInfoForm().validate_for_api().data_
    Announcement.modify(id_, **form)
    return Success('Modify announcement success')
