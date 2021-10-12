from marshmallow import fields
from marshmallow.validate import And, Length, Email, Regexp
from . import ma
from .validation import CUSTOM_ERRORS, is_unique
from .models import User, UserConfirmation


class UserSchema(ma.SQLAlchemyAutoSchema):
	username = fields.Str(validate=And(
		Length(min=1, max=80, error=CUSTOM_ERRORS['username']),
		is_unique('username')
	))
	email = fields.Str(validate=And(Email(), is_unique('email')))
	password = fields.Str(validate=Regexp(
		r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$',
		error=CUSTOM_ERRORS['password']
	))

	class Meta:
		model = User
		load_instance = True
		load_only = ('password',)
		dump_only = ('is_active',)


class LoginSchema(ma.Schema):
	username = fields.Str()
	password = fields.Str()


class UserConfirmationSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = UserConfirmation
		load_instance = True
		include_fk = True
		load_only = ('user',)
		dump_only = ('id', 'expires_at', 'confirmed')
