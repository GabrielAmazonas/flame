from flask import Flask, jsonify, request, make_response
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import connect
from models.user import User
from database_config import DatabaseConfig

import jwt

import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = DatabaseConfig

db = MongoEngine(app)

@app.route('/register', methods=["POST"])
def register():
    #create user model
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


if __name__ == "__main__":
    app.run()
    