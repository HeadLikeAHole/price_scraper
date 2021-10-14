from flask import request
from flask_restful import abort
from marshmallow import ValidationError
from .models import User
from .strings import get_text


def get_data_or_400(schema):
    try:
        return schema.load(request.get_json())
    except ValidationError as err:
        abort(400, errors=err.messages)


def is_unique(name):
    def validator(value):
        kwargs = {name: value}

        if User.query.filter_by(**kwargs).first():
            raise ValidationError(get_text('unique_value'))
    return validator
