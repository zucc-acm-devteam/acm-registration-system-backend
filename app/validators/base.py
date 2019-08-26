from flask import request
from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict

from app.libs.error_code import ParameterException


class BaseForm(FlaskForm):
    def __init__(self):
        data = MultiDict(request.get_json(silent=True))
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            raise ParameterException(msg=self.errors)
        return self

    @property
    def data_(self):
        data = dict()
        for key, value in self.__dict__.items():
            try:
                data[key] = value.data
            except AttributeError:
                pass
        return data
