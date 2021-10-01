import re
from .models import User


def username_validator(value):
    if not isinstance(value, str):
        raise ValueError('Username should be of type string.')

    if len(value) < 1 or len(value) > 80:
        raise ValueError('Username should be from 1 to 80 characters long.')

    if User.query.filter_by(username=value).first():
        raise ValueError('Username already exists. Try a different one.')

    return value


def email_validator(value):
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(regex, value):
        raise ValueError('Invalid email.')

    if User.query.filter_by(email=value).first():
        raise ValueError('Email already exists. Try a different one.')

    return value
