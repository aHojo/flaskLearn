# /c/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio/Shared/Python39_64/python.exe
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from security import authenticate, identity as identity_function

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)

app.secret_key = "kairihojo"
# app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
api = Api(app) # not creating /auth for us

@app.before_first_request
def create_tables():
    db.create_all()


"""
JWT creates a new endpoint called /auth
send username and password
passes it to authenticate
return jwt token

calls the identity function, gets the user id out and then we are authenticated
"""
#jwt = JWT(app, authenticate, identity_function)
jwt = JWTManager(app)


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    print(jwt_payload, jwt_header)
    return jwt_payload['jti'] in BLACKLIST # defined in the package

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # instead of hard-coding you should read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401
@jwt.invalid_token_loader # when the Authorization token is not valid
def invalid_token_callback(error):
    return jsonify({
        'description': "Signature verification failed",
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': "Request does not contain an access token",
        "error": "unauthorized_token"
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': "The token is not fresh",
        "error": "fresh_token_required"
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': "The token has been revoked",
        "error": "token_revoked"
    }), 401
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
# #     Remember that the identity should be what you've returned by the authenticate()
# # function,
#     return jsonify({
#         'access_token': access_token.decode('utf-8'),
#         'user_id': identity.id
#     })
# @jwt.jwt_error_handler
# def customized_error_handler(error):
#  return jsonify({
#  'message': error.description,
#  'code': error.status_code
#  }), error.status_code


api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/item/kairi
api.add_resource(ItemList, '/items') # http://localhost:5000/item/kairi
api.add_resource(UserRegister, "/register")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000)