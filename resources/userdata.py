from flask import request
from flask_jwt_extended import get_current_user
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models import User, Scrap
from playhouse.shortcuts import model_to_dict
from playhouse.flask_utils import PaginatedQuery


class UserData(Resource):
    @jwt_required
    def get(self):

        userParser = reqparse.RequestParser()
        userParser.add_argument('id')
        userParser.add_argument('email')
        userParser.add_argument('password')
        userParser.add_argument('name')
        userParser.add_argument('GRNo')
        userParser.add_argument('dept')
        userParser.add_argument('dob')
        userParser.add_argument('quote')
        userParser.add_argument('photo')
        userParser.add_argument('scraps')

        data = userParser.parse_args()

        if data["id"] is None:
            user = get_current_user()
            current_user_flag = 1
        else:
            user = User.get(User.id == data['id'])
            current_user_flag = 0

        userjson = {"id": user.id}

        if data['email']:
            userjson["email"] = user.email
        if data['name']:
            userjson["name"] = user.name
        if data['GRNo']:
            userjson["GRNo"] = user.gr
        if data['dept']:
            userjson["dept"] = user.dept
        if data['dob']:
            userjson["dob"] = user.dob
        if data['quote']:
            userjson["quote"] = user.quote
        if data['photo']:
            userjson["photo"] = user.photo
        if data['scraps']:
            scrap = Scrap.select().where(user.id == Scrap.posted_to_id)
            scraps = [model_to_dict(s) for s in scrap]
            try:
                for x in scraps:
                    x["posted_by"].pop('email')
                    x["posted_by"].pop('password')
                    x["posted_by"].pop('joined_at')
                    x["posted_by"].pop('quote')
                    x["posted_by"].pop('photo')
                    x["posted_by"].pop('gr')
                    x["posted_by"].pop('dob')
                    x["posted_by"].pop('dept')

                    x["posted_to"].pop('email')
                    x["posted_to"].pop('password')
                    x["posted_to"].pop('joined_at')
                    x["posted_to"].pop('quote')
                    x["posted_to"].pop('photo')
                    x["posted_to"].pop('gr')
                    x["posted_to"].pop('dob')
                    x["posted_to"].pop('dept')

                    if current_user_flag == 0:  # meaning the user is NOT requesting scraps of himself
                        if not x["visibility"]:
                            scraps.remove(x)
            except:
                pass
            userjson['scraps'] = scraps

        return userjson

    @jwt_required
    def put(self):
        updateParser = reqparse.RequestParser()
        updateParser.add_argument('email')
        updateParser.add_argument('password')
        updateParser.add_argument('name')
        updateParser.add_argument('GRNo')
        updateParser.add_argument('dept')
        updateParser.add_argument('dob')
        updateParser.add_argument('quote')
        current_user = get_current_user()

        data = updateParser.parse_args()

        try:
            if data['email'] is not None:
                return {"error": "Cannot change email"}
            elif data['name'] is not None:
                User.update(
                    name=data['name']
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
