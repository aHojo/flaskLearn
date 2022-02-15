from multiprocessing import connection
import sqlite3

from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jti

from blacklist import BLACKLIST
from models.user import UserModel




class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field can't be blank")
    parser.add_argument("password", type=str, required=True, help="This field can't be blank")

    def post(self):

        data = UserRegister.parser.parse_args()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        user = UserModel.find_by_username(data["username"])

        if user:
            return {"message": "User already exists"}, 400

        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data["username"], data["password"]))

        # connection.commit()
        # connection.close()
        # return {"message": "User successfully registered"}, 201

        # user = UserModel(data['username'], data['password']) - same as below just unpacking
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User successfully registered"}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "user deleted"}, 200

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field can't be blank")
    parser.add_argument("password", type=str, required=True, help="This field can't be blank")

    @classmethod
    def post(cls):
        # get data from parser
        data = cls.parser.parse_args()
        # find the user in the database
        user = UserModel.find_by_username(data['username'])
        # check password
        # create access token
        # create refresh token
        # return them
        if user and safe_str_cmp(user.password, data['password']):
            # identity= is what the identity() function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "invalid creds"}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "User logged out"}, 200

class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200