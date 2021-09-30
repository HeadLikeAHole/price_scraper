import re


def length_validator(data_type, min_length=None, max_length=None):
    def validate(value, name):
        if not isinstance(value, data_type):
            raise ValueError(f'Invalid data type for {name}')

        if min_length and len(value) < min_length:
            raise ValueError(f'{name} must be at least {min_length} characters long')

        if max_length and len(value) > max_length:
            raise ValueError(f'{name} must not exceed {max_length} characters')

    return validate


def email_validator(value):
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    if not re.match(regex, value):
        raise ValueError('Invalid email')


def password_validator(value):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"

    if not re.match(regex, value):
        raise ValueError('Password should have at least one number, one uppercase and one lowercase character, one special symbol and be at least 8 characters long.')