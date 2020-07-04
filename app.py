from flask import Flask, jsonify, g
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import resources
import models\
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

app.secret_key = 'rajrajhanskbrtgw490kjs!'
app.config['JWT_SECRET-KEY'] = 'rajrajhanskbrtgw490kjs!'

jwt = JWTManager(app)


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


api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogin, '/login')

if __name__ == "__main__":
    app.debug = True
    models.initialize()
    app.run()
