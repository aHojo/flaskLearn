# /c/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio/Shared/Python39_64/python.exe
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity as identity_function

from resources.user import UserRegister
from resources.item import Item, ItemList

from db import db

app = Flask(__name__)
app.secret_key = "kairihojo"
app.config['JWT_AUTH_URL_RULE'] = '/login'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app)

"""
JWT creates a new endpoint called /auth
send username and password
passes it to authenticate
return jwt token

calls the identity function, gets the user id out and then we are authenticated
"""
jwt = JWT(app, authenticate, identity_function)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
#     Remember that the identity should be what you've returned by the authenticate()
# function,
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })
@jwt.jwt_error_handler
def customized_error_handler(error):
 return jsonify({
 'message': error.description,
 'code': error.status_code
 }), error.status_code


api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/item/kairi
api.add_resource(ItemList, '/items') # http://localhost:5000/item/kairi
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000)