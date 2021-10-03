import re
from .models import User


def is_unique(name, value):
    kwargs = {name: value}

    if User.query.filter_by(**kwargs).first():
        raise ValueError(f'{name} already exists. Try a different one.')


def username_validator(value, name):
    if not isinstance(value, str):
        raise ValueError('Username should be of type string.')

    if len(value) < 1 or len(value) > 80:
        raise ValueError('Username should be from 1 to 80 characters long.')

    is_unique(name, value)

    return value


def email_validator(value, name):
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(regex, value):
        raise ValueError('Invalid email.')

    is_unique(name, value)

    return value
