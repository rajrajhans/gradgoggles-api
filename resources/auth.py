from flask import request
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
import boto3
import os
import json
from models import User

regparser = reqparse.RequestParser()
regparser.add_argument('email', help='Email cannot be blank', required=True)
regparser.add_argument('password', help='Password cannot be blank', required=True)
regparser.add_argument('fullName', help='Full Name cannot be blank', required=True)
regparser.add_argument('GRNo')
regparser.add_argument('dept')
regparser.add_argument('dob')
regparser.add_argument('quote')
regparser.add_argument('photo')

loginparser = reqparse.RequestParser()
loginparser.add_argument('email', help='Email cannot be blank', required=True)
loginparser.add_argument('password', help='Password cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = regparser.parse_args()
        if User.get_or_none(User.email == data['email']) is not None:
            return {"error": "User already exists"}
        User.create_user(email=data['email'],
                         password=data['password'],
                         name=data['fullName'],
                         gr=data['GRNo'],
                         dept=data['dept'],
                         dob=data['dob'],
                         quote=data['quote'],
                         photo=data['photo']
                         )

        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        return {
            'name': data['fullName'],
            'photo': 'nothing',  # todo
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class UserLogin(Resource):
    def post(self):
        try:
            data = loginparser.parse_args()

            user = User.get_or_none(User.email == data['email'])

            if user is None:  # User doesnt exist, send to registration (todo)
                return {'error': 'Email or password does not match'}
            else:
                if check_password_hash(user.password, data['password']):
                    access_token = create_access_token(identity=data['email'])
                    refresh_token = create_refresh_token(identity=data['email'])

                    return {
                        'name': user.name,
                        'photo': user.photo,
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                else:
                    return {'error': 'Email or password does not match'}

        except:
            return {"exception": "login error"}


class SignS3Request(Resource):
    def get(self):
        S3_BUCKET = os.environ.get('S3_BUCKET')
        S3_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
        S3_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')

        file_name = request.args.get('file_name')
        file_type = request.args.get('file_type')
        s3 = boto3.client('s3',
                          aws_access_key_id=S3_KEY,
                          aws_secret_access_key=S3_SECRET)

        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )
        return json.dumps({
            'data': presigned_post,
            'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
        })
