import logging
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Api
from custom_json_encoder import custom_json_output
import models
from resources import auth, userdata, scraps, email_verification
import os

app = Flask(__name__)
api = Api(app)
api.representations.update({
    'application/json': custom_json_output
})
cors = CORS(app)
# logging.getLogger('flask_cors').level = logging.DEBUG

app.secret_key = os.environ["APP_SECRET"]
app.config['JWT_SECRET-KEY'] = os.environ["JWT_SECRET"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)


@jwt.user_loader_callback_loader
def userLoader(identity):
    try:
        return models.User.get(models.User.email == identity)
    except:
        return None


@app.before_request
def before_request():
    # connect to the database
    g.db = models.DATABASE_proxy
    g.db.connection()
    g.user = get_jwt_identity()
    # logging
    # if request.get_data():
    #     print("\nRequest Body:", request.get_data(), '\n')
    #     # print("\nRequest Headers:", request.headers, '\n')
    # if request.args:
    #     print("\nRequest Args:", request.args, '\n')


@app.after_request
def after_request(response):
    # close database connection
    g.db.close()
    return response


@app.route('/')
@jwt_required
def index():
    return jsonify({"hi": "raj"})


api.add_resource(auth.UserRegistration, '/register')
api.add_resource(auth.UserLogin, '/login')
api.add_resource(auth.SignS3Request, '/sign_s3')
api.add_resource(auth.ChangePassword, '/change_password')
api.add_resource(auth.ForgotPassword, '/forgotPassword')
api.add_resource(auth.ForgotPasswordSendMail, '/forgotPasswordSendMail')
api.add_resource(email_verification.ConfirmUser, '/verify')
api.add_resource(email_verification.ResendConfirmationEmail, '/resend_email')
api.add_resource(email_verification.CheckUserVerification, '/check_verification')

api.add_resource(userdata.GetAllUserData, '/users')
api.add_resource(userdata.GetAllUserDataTen, '/usersandroid')
api.add_resource(userdata.UserData, '/user')
api.add_resource(userdata.SearchUserData, '/search')
api.add_resource(userdata.SearchUserDataPaginated, '/searchPaginated')

api.add_resource(scraps.CreateScrap, '/createScrap')
api.add_resource(scraps.DeleteScrap, '/deleteScrap')
api.add_resource(scraps.ToggleScrapVisibility, '/toggleScrapVisibility')

if __name__ == "__main__":
    if 'HEROKU' in os.environ:
        app.debug = False
    else:
        app.debug = True
    models.initialize()
    app.run()
