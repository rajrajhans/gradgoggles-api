from flask_jwt_extended import get_current_user
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models import User
from playhouse.shortcuts import model_to_dict
from playhouse.flask_utils import PaginatedQuery


class GetCurrentUserData(Resource):
    @jwt_required
    def get(self):
        current_user = get_current_user()
        return {
            "email": current_user.email,
            "fullName": current_user.name,
            "quote": current_user.quote,
            "photo": current_user.photo,
            "gr": current_user.gr,
            "dob": current_user.dob,
            "dept": current_user.dept
        }


class GetAllUserData(Resource):
    @jwt_required
    def get(self):
        usersSelect = User.select(User.id, User.name, User.email, User.quote, User.photo, User.gr, User.dob, User.dept)
        pq = PaginatedQuery(usersSelect, paginate_by=10)
        users = [model_to_dict(user) for user in pq.get_object_list()]

        return users


getOneUserParser = reqparse.RequestParser()
getOneUserParser.add_argument('userid', help='User ID is required', required=True)


class GetOneUserData(Resource):
    @jwt_required
    def get(self):
        data = getOneUserParser.parse_args()
        userSelect = User.select(User.id, User.name, User.email, User.quote, User.photo, User.gr, User.dob,
                                 User.dept).where(User.id == data['userid'])
        user = [model_to_dict(user) for user in userSelect]

        return user
