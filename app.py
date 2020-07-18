import logging
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Api
from custom_json_encoder import custom_json_output
import models
from resources import auth
from resources import userdata
import os

app = Flask(__name__)
api = Api(app)
api.representations.update({
    'application/json': custom_json_output
})
cors = CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG

app.secret_key = 'rajrajhanskbrtgw490kjs!'
app.config['JWT_SECRET-KEY'] = 'rajrajhanskbrtgw490kjs!'
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
api.add_resource(userdata.GetCurrentUserData, '/getCurrentUserData')
api.add_resource(userdata.GetAllUserData, '/getAllUserData')
api.add_resource(userdata.GetOneUserData, '/getOneUserData')

if __name__ == "__main__":
    if 'HEROKU' in os.environ:
        app.debug = False
    else:
        app.debug = True
    models.initialize()
    app.run()
