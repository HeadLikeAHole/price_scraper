from flask import send_from_directory

from backend import app


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')