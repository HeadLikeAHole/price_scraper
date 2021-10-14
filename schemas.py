from marshmallow import fields
from marshmallow.validate import And, Length, Email, Regexp
from marshmallow import pre_dump

from . import ma
from .validation import is_unique
from .models import User, UserConfirmation
from .strings import get_text


class UserSchema(ma.SQLAlchemyAutoSchema):
	username = fields.Str(validate=And(
		Length(min=1, max=80, error=get_text('username_length')),
		is_unique('username')
	))
	email = fields.Str(validate=And(Email(), is_unique('email')))
	password = fields.Str(validate=Regexp(
		r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$',
		error=get_text('password_regex')
	))

	class Meta:
		model = User
		load_instance = True
		load_only = ('password',)
		dump_only = ('user_confirmation',)

	# dump only the latest confirmation
	@pre_dump
	def _pre_dump(self, user):
		user.user_confirmation = [user.latest_confirmation]
		return user


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
