from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.secret_key = 'rajrajhanskbrtgw490kjs!'
app.config['JWT_SECRET-KEY'] = 'rajrajhanskbrtgw490kjs!'

jwt = JWTManager(app)


@app.route('/')
def index():
    return jsonify({"hi": "raj"})


if __name__ == "__main__":
    app.debug = True
    app.run()
