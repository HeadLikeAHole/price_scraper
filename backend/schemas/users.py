from marshmallow import fields
from marshmallow.validate import And, Length, Email, Regexp
from marshmallow import pre_dump

from backend import ma
from backend.validation import is_unique
from backend.models.users import User
from backend.translation import get_text as _


class UserSchema(ma.SQLAlchemyAutoSchema):
	username = fields.Str(validate=And(
		Length(min=1, max=80, error=_('invalid_username')),
		is_unique('username')
	))
	email = fields.Str(validate=And(Email(), is_unique('email')))
	password = fields.Str(validate=Regexp(
		r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$',
		error=_('invalid_password')
	))

	class Meta:
		model = User
		load_instance = True
		load_only = ('password',)
		dump_only = ('registration_confirmation',)

	# dump only the latest confirmation
	@pre_dump
	# "many" is always passed to the decorated method
	def _pre_dump(self, user, many):
		# registration_confirmation must be an iterable
		user.registration_confirmation = [user.latest_confirmation]
		return user


class LoginSchema(ma.Schema):
	username = fields.Str()
	password = fields.Str(validate=Regexp(
		r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$',
		error=_('invalid_password')
	))
