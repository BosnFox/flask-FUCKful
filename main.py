from flask_restful import abort, Api, Resource
from data import db_session
from data.__all_models import users
from flask import jsonify, Flask


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.id == user_id).first()
        if not user:
            abort(404, message=f"{user_id} не найден")
        return jsonify(
            {'user': user.to_dict(
                only=('id',
                      'login',
                      'registration_date',
                      'description',
                      'private_account',
                      'avatar_photo_id')
            )}
        )


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        userss = session.query(users.User).all()
        return jsonify(
            {'users': [
                user.to_dict(
                    only=(
                        'id',
                        'login',
                        'registration_date',
                        'description',
                        'private_account',
                        'avatar_photo_id'
                    )
                ) for user in userss
            ]}
        )


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)
api.add_resource(UsersListResource, '/api/users')
api.add_resource(UsersResource, '/api/users/<int:user_id>')
