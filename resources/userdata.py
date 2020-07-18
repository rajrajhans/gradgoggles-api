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


class UpdateCurrentUserData(Resource):
    @jwt_required
    def put(self):
        updateParser = reqparse.RequestParser()
        updateParser.add_argument('email')
        updateParser.add_argument('password')
        updateParser.add_argument('fullName')
        updateParser.add_argument('GRNo')
        updateParser.add_argument('dept')
        updateParser.add_argument('dob')
        updateParser.add_argument('quote')
        current_user = get_current_user()

        data = updateParser.parse_args()

        try:
            if data['email'] is not None:
                return {"error": "Cannot change email"}
            elif data['fullName'] is not None:
                User.update(
                    name=data['fullName']
                ).where(
                    User.id == current_user.id
                ).execute()
            elif data['GRNo'] is not None:
                User.update(
                    gr=data['GRNo']
                ).where(
                    User.id == current_user.id
                ).execute()
            elif data['dept'] is not None:
                User.update(
                    dept=data['dept']
                ).where(
                    User.id == current_user.id
                ).execute()
            elif data['dob'] is not None:
                User.update(
                    dob=data['dob']
                ).where(
                    User.id == current_user.id
                ).execute()
            elif data['quote'] is not None:
                User.update(
                    quote=data['quote']
                ).where(
                    User.id == current_user.id
                ).execute()
            return {
                "success": "Updation Successful"
            }
        except:
            return {
                "error": "Error: Check Data Types"
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
