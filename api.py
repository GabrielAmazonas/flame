from flask import Flask, jsonify, request, make_response
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import connect
from functools import wraps

import jwt
import json
import datetime

from models.user import User
from config import DatabaseConfig, JwtConfig

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = DatabaseConfig

db = MongoEngine(app)

#Decorator creation
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'No token was provided'})
        try:
            data = jwt.decode(token, JwtConfig['key'])
        except:
            return jsonify({'message': 'Token is invalid'})

        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=["POST"])
def register():
    request_data_decoded = request.data.decode("utf-8")
    request_data_dict = json.loads(request_data_decoded, encoding="utf-8")

    email = request_data_dict["Email"]
    password = request_data_dict["Password"]

    #instantiates a new user only if the username is not used.

    existing_user = User.objects(email=email).first()

    if existing_user is None:
        hashpass = generate_password_hash(password, method='sha256')
        user = User()
        user.email = email
        user.password = hashpass
        user.save()
        return 'User registered.'
    else:
        return 'User already exists.'


@app.route('/login', methods=["POST"])
def login():
    response = {"success": True}

    request_data_decoded = request.data.decode("utf-8")
    request_data_dict = json.loads(request_data_decoded, encoding="utf-8")

    email = request_data_dict["Email"]
    password = request_data_dict["Password"]

    check_user = User.objects(email=email).first()

    if check_user:
        if check_password_hash(check_user['password'], password):
            token = jwt.encode({'user': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, JwtConfig['key'], algorithm='HS256')

            #The generated token is a bytes object
            response["token"] = token.decode('UTF-8')
            return json.dumps(response)

    return make_response('Access denied', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'TOKEN Validated.'})


if __name__ == "__main__":
    app.run()
    