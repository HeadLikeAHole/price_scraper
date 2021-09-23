from flask import send_from_directory
from flask_restful import Resource
from . import app, api


@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')
