from flask import request
from flask_restful import abort
from marshmallow import ValidationError

from backend.models import User
from backend.translation import get_text as _


def get_data_or_400(schema):
    try:
        return schema.load(request.get_json())
    except ValidationError as err:
        abort(400, errors=err.messages)


def is_unique(name):
    def validator(value):
        kwargs = {name: value}

        if User.query.filter_by(**kwargs).first():
            raise ValidationError(_('not_unique').format(name.capitalize()))
    return validator
