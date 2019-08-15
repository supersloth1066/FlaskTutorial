from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='this field cannot be left blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='this field cannot be left blank'
    )

    def post(self):
        req_data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(req_data['username'])
        if user:
            return {'message':'user already exists'}, 400
        else:
            user = UserModel(**req_data)
            user.save_to_db()
            return {'message' : 'user created'}, 201