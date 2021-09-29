from flask import send_from_directory
from flask_restful import Resource, reqparse, fields, marshal_with
from . import app, api, bcrypt, db


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.Integer,
    'password': fields.Integer
}

user_create_args = reqparse.RequestParser()
user_create_args.add_argument('username', type=str, help="Username is required", required=True)
user_create_args.add_argument('email', type=str, help="Email is required", required=True)
user_create_args.add_argument("password", type=str, help="Password is required", required=True)

class Users(Resource):
    # def get(self, todo_id):
    #     return {todo_id: todos[todo_id]}

    @marshal_with(user_fields)
    def post(self, todo_id):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return {'data': user}

api.add_resource(TodoSimple, '/<string:todo_id>')
