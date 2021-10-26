import os

from flask import g
from flask_oauthlib.client import OAuth


oauth = OAuth()

vk_oauth = oauth.remote_app(
	'vk',
	consumer_key=os.environ.get('VK_APP_ID'),
	consumer_secret=os.environ.get('VK_SECURE_KEY'),
	base_url='https://api.vk.com/method/',
	access_token_url='https://oauth.vk.com/access_token',
	access_token_method='POST',
	authorize_url='https://oauth.vk.com/authorize',
	request_token_params={'scope': 'email'},
	request_token_url=None,
)


@vk_oauth.tokengetter
def get_vk_oauth_token():	
	if 'access_token' in g:
		return g.access_token
