from flask_jwt_extended import get_current_user
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models import User, Scrap
from playhouse.shortcuts import model_to_dict
from playhouse.flask_utils import PaginatedQuery


# expects 'posted_to_id' & 'content in body
class CreateScrap(Resource):
    @jwt_required
    def post(self):
        scrapParser = reqparse.RequestParser()
        scrapParser.add_argument('posted_to_id', help='posted_to_id not present in the request body', required=True)
        scrapParser.add_argument('content', help='content not present in the request body', required=True)

        current_user = get_current_user()

        if not current_user.isVerified:
            return{"msg":"Please verify your account to create scrap"}

        data = scrapParser.parse_args()

        try:
            posted_by_user = User.get(User.id == current_user.id)
            posted_to_user = User.get(User.id == data['posted_to_id'])
        except:
            return{"msg": "User not found"}

        try:
            Scrap.create(
                posted_by=posted_by_user,
                posted_to=posted_to_user,
                content=data['content']
            )
            return {"msg": "Scrap created successfully"}
        except:
            return {"msg": "Error creating Scrap"}


class ToggleScrapVisibility(Resource):
    @jwt_required
    def put(self):
        hideScrapParser = reqparse.RequestParser()
        hideScrapParser.add_argument('id', help='scrap id not present in the request body', required=True)

        current_user = get_current_user()
        data = hideScrapParser.parse_args()

        try:
            scrap = Scrap.get((Scrap.id == data['id']) & (Scrap.posted_to_id == current_user.id))

            if scrap.visibility:
                Scrap.update(
                    visibility=False
                ).where(
                    (Scrap.id == data['id']) & (Scrap.posted_to_id == current_user.id)
                ).execute()
            else:
                Scrap.update(
                    visibility=True
                ).where(
                   (Scrap.id == data['id']) & (Scrap.posted_to_id == current_user.id)
                ).execute()

            return {"msg": "Updation successful"}

        except:
            return{"msg": "there was an error hiding the scrap"}


class DeleteScrap(Resource):
    @jwt_required
    def put(self):
        delScrapParser = reqparse.RequestParser()
        delScrapParser.add_argument('id', help='scrap id not present in the request body', required=True)

        current_user = get_current_user()
        data = delScrapParser.parse_args()

        try:
            scrap = Scrap.get((Scrap.id == data['id']) & (Scrap.posted_to_id == current_user.id))

            scrap.delete_instance()

            return {"msg": "Updation successful"}

        except:
            return {"msg": "there was an error in deleting the scrap"}