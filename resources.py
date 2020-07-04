from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from models import User

parser = reqparse.RequestParser()
parser.add_argument('email', help='Email cannot be blank', required=True)
parser.add_argument('password', help='Password cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if User.get_or_none(User.email == data['email']) is not None:
            return {"error": "User already exists1234"}
        User.create_user(email=data['email'], password=data['password'])

        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        return {
            'email': data['email'],
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class UserLogin(Resource):
    def post(self):
        try:
            data = parser.parse_args()

            user = User.get_or_none(User.email == data['email'])

            if user is None:  # User doesnt exist, send to registration (todo)
                return {'error': 'Email or password does not match'}
            else:
                if check_password_hash(user.password, data['password']):
                    access_token = create_access_token(identity=data['email'])
                    refresh_token = create_refresh_token(identity=data['email'])

                    return {
                        'email': data['email'],
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                else:
                    return {'error': 'Email or password does not match'}

        except:
            return Exception("Login Error")
