import os

from flask_oauthlib.client import OAuth


oauth = OAuth()

vk_oauth = oauth.remote_app(
	'vk',
	consumer_key = os.environ.get('VK_CLIENT_ID'),
	consumer_secret = os.environ.get('VK_CLIENT_SECRET'),
	base_url='https://oauth.vk.com',
	access_token='https://oauth.vk.com/access_token',
	authorize_url= 'https://oauth.vk.com/authorize',
	request_token_params = {'scope': 'email'},
	request_token_url= None
)




# app = Flask(__name__, static_folder='static', static_url_path='static')
# app.config.from_envvar('SETTINGS')

# oauth = OAuth()
# vk_client = VKClient(api_url=app.config['VK_API_URL'])
# db = Database(db_name=app.config['DB_NAME'], db_path=app.config['DB_PATH'])


# vk_oauth = oauth.remote_app('vk',
# 	base_url				= app.config['VK_OAUTH_URL'],	
# 	consumer_key			= app.config['VK_APP_ID'],
# 	consumer_secret			= app.config['VK_APP_SECRET'],
# 	access_token_url		= '/access_token',
# 	authorize_url			= '/authorize',
# 	request_token_url		= None,	
# 	request_token_params	= {'scope': 'email'}
# )

# @vk_oauth.tokengetter
# def get_vk_oauth_token():	
# 	return session.get('oauth_token')


# class AuthorizationError(Exception):
# 	pass

# def redirect_if_error(function):
# 	@functools.wraps(function)