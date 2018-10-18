from flask import Flask, jsonify, request, make_response
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import jwt
import json
import datetime

# Import collection models
from models.user import User
from models.request_log import RequestLog

app = Flask(__name__)

#Environment management settings, defaults to dev stage
app.config.from_object('db_config')
app.config.from_object('jwt_config')

#Check the environment variables
app.config.from_envvar('DB_CONFIG', silent=True)
app.config.from_envvar('JWT_CONFIG', silent=True)

db = MongoEngine(app)

#Decorator creation
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #Initializes an empty token variable
        token = ''

        #Checks for the Authorization Header inside the request
        authorization_header = request.headers["Authorization"]

        #If authorization header is truthy and contains Bearer, extract the following token
        if(authorization_header and 'Bearer ' in authorization_header):
            token = authorization_header.split('Bearer ')[1]

        if not token:
            return make_response('Access denied', 401, {'WWW-Authenticate' : 'Basic realm="No token was provided"'})
        try:
            data = jwt.decode(token, app.config['JWT_CONFIG']['key'], {'verify_exp': True})

            #Decodes the incoming request body to UTF-8
            request_data_decoded = request.data.decode("utf-8")

            #Converts the request.headers dict to a string
            request_headers_decoded = str(request.headers)

            #Saves the log to the database
            request_log = RequestLog()
            request_log.user = data['user']
            request_log.request_body = request_data_decoded
            request_log.request_headers = request_headers_decoded
            request_log.save()
        except:
             return make_response('Access denied', 401, {'WWW-Authenticate' : 'Basic realm="Invalid token"'})

        return f(request_log, *args, **kwargs)
    return decorated

@app.route('/', methods=["POST", "GET"])
def healthcheck():
    return "Hello AWS Lambda!"

@app.route('/register', methods=["POST"])
def register():

    #Decodes the incoming request to UTF-8
    request_data_decoded = request.data.decode("utf-8")

    #Transforms the decoded request to a JSON object
    request_data_dict = json.loads(request_data_decoded, encoding="utf-8")

    try:

        #This parameters required.
        email = request_data_dict["Email"]
        password = request_data_dict["Password"]

        #Instantiates a new user only if the username is not used.
        existing_user = User.objects(email=email).first()

        if existing_user is None:
            hashpass = generate_password_hash(password, method='sha256')
            user = User()
            user.email = email
            user.password = hashpass
            user.save()
            return make_response('User registered', 200)
        else:
            return make_response('User already exists', 400)
    except:
        return make_response('An error ocurred. Please, check the provided parameters.', 400)


@app.route('/login', methods=["POST"])
def login():
    response = {"success": True}

    request_data_decoded = request.data.decode("utf-8")
    request_data_dict = json.loads(request_data_decoded, encoding="utf-8")

    email = request_data_dict["Email"]
    password = request_data_dict["Password"]

    check_user = User.objects(email=email).first()

    if check_user:
        # Checks if the provided password matches with the database password.
        if check_password_hash(check_user['password'], password):

            token = jwt.encode({'user': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, app.config['JwtConfig']['key'], algorithm='HS256')

            #The generated token is a bytes object
            response["token"] = token.decode('UTF-8')
            return jsonify(response)

    return make_response('Access denied', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/protected', methods=["POST"])
@token_required
def protected(request_log):
    return jsonify({'message' : 'TOKEN Validated.'})

if __name__ == "__main__":
    app.run()
