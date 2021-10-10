from flask import request
from flask_restful import abort
from marshmallow import ValidationError
from .models import User


CUSTOM_ERRORS = {
    'username': 'username must be between 1 and 80 characters long.',
    'password': 'password must contain at least one number, one uppercase and one lowercase character, one special symbol and be at least 8 characters long.'
}


def get_data_or_400(schema):
    try:
        return schema.load(request.get_json())
    except ValidationError as err:
        abort(400, errors=err.messages)


def is_unique(name):
    def validator(value):
        kwargs = {name: value}

        if User.query.filter_by(**kwargs).first():
            raise ValidationError(f'{name} already exists. Try a different one.')
    return validator
