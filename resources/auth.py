from datetime import datetime
from botocore.config import Config
from flask import request, render_template, make_response
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_current_user
from flask_restful import Resource, reqparse
import boto3
import os
import json
from models import User
from resources import email_verification

class UserRegistration(Resource):
    def post(self):
        regparser = reqparse.RequestParser()
        regparser.add_argument('email', help='Email cannot be blank', required=True)
        regparser.add_argument('password', help='Password cannot be blank', required=True)
        regparser.add_argument('fullName', help='Full Name cannot be blank', required=True)
        regparser.add_argument('GRNo')
        regparser.add_argument('dept')
        regparser.add_argument('dob')
        regparser.add_argument('quote')
        regparser.add_argument('photo')
        regparser.add_argument('is2020')
        data = regparser.parse_args()
        if User.get_or_none(User.email == data['email']) is not None:
            return {"error": "User already exists"}
        try:
            formatted_dob = datetime.strptime(data['dob'], '%d-%m-%Y')
        except:
            formatted_dob = None
        if data['is2020'] == '2020':
            is2020 = True
        else:
            is2020 = False
        user = User.create_user(email=data['email'],
                         password=data['password'],
                         name=data['fullName'],
                         gr=data['GRNo'],
                         dept=data['dept'],
                         dob=formatted_dob,
                         quote=data['quote'],
                         photo=data['photo'],
                         is2020=is2020
                         )

        token = email_verification.generate_confirmation_token(data['email'])
        email_verification.send_confirmation_mail(data['email'], data['fullName'], token)
        print("Email sent to ", data['email'])

        access_token = create_access_token(identity=data['email'])
        refresh_token = create_refresh_token(identity=data['email'])

        return {
            'id': user.id,
            'name': data['fullName'],
            'photo': data['photo'],
            'access_token': access_token,
            'is2020': is2020,
            'error': 'none'
        }


class UserLogin(Resource):
    def post(self):
        try:
            loginparser = reqparse.RequestParser()
            loginparser.add_argument('email', help='Email cannot be blank', required=True)
            loginparser.add_argument('password', help='Password cannot be blank', required=True)
            data = loginparser.parse_args()

            user = User.get_or_none(User.email == data['email'])

            if user is None:  # User doesnt exist, send to registration (todo)
                return {'error': 'Email or password does not match'}
            else:
                if check_password_hash(user.password, data['password']):
                    access_token = create_access_token(identity=data['email'])
                    refresh_token = create_refresh_token(identity=data['email'])

                    return {
                        'id': user.id,
                        'name': user.name,
                        'photo': user.photo,
                        'access_token': access_token,
                        'is2020': user.is2020,
                        'isVerified': user.isVerified,
                        'error': 'none'
                    }
                else:
                    return {'error': 'Email or password does not match'}

        except:
            return {"exception": "login error"}


class SignS3Request(Resource):
    def get(self):
        if 'HEROKU' in os.environ:
            S3_BUCKET = os.environ["S3_BUCKET"]
            S3_KEY = os.environ["AWS_ACCESS_KEY_ID"]
            S3_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]
            print("s3key", S3_KEY)
            print("s3bucket", S3_BUCKET)
            print("s3secret", S3_SECRET)

        else:
            S3_BUCKET = os.environ["S3_BUCKET"]
            S3_KEY = os.environ["AWS_ACCESS_KEY_ID"]
            S3_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]

        file_name = request.args.get('file_name')
        file_type = request.args.get('file_type')
        s3 = boto3.client('s3',
                          region_name="ap-south-1",
                          aws_access_key_id=S3_KEY,
                          aws_secret_access_key=S3_SECRET,
                          config=Config(signature_version='s3v4'))

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


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('current_password')
        parser.add_argument('new_password')

        data = parser.parse_args()
        user = get_current_user()

        if check_password_hash(user.password, data['current_password']):
            User.update(
                password=generate_password_hash(data['new_password'])
            ).where(
                User.id == user.id
            ).execute()
            return {'msg': 'Password Changed'}
        else:
            return {'msg': 'Password does not match'}


class ForgotPassword(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')

        data = parser.parse_args()

        try:
            email = email_verification.confirm_token(data['token'])
            if not email:
                return {"msg": "Token Expired or Invalid"}
        except:
            return {"msg": "Token Expired or Invalid"}  # TODO: Show the User a Page

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('forgotPassword.html', email=email), 200, headers)

    def post(self):
        data = request.form
        User.update(
            password=generate_password_hash(data['new_password'])
        ).where(
            User.email == data['email']
        ).execute()

        return {"msg": "Password Changed"}


class ForgotPasswordSendMail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')

        data = parser.parse_args()
        email = data['email']
        user = User.get_or_none(User.email == email)

        if user:
            token = email_verification.generate_confirmation_token(email)
            email_verification.send_passwordreset_mail(email, user.name, token)
            print("reset mail sent to", email)
            return {"msg": "email sent"}
        else:
            return {"msg": "email does not exist, please sign up"}
