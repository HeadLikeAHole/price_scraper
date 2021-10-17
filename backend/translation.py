import json


default_locale = 'en-us'
cached_strings = {}


def refresh():
	with open(f'backend/locales/{default_locale}.json') as file:
		global cached_strings
		cached_strings = json.load(file)


def get_text(name):
	return cached_strings[name]


def set_default_locale(locale):
	global default_locale
	default_locale = locale


refresh()
