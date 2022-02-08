from multiprocessing import connection
import sqlite3

from flask_restful import Resource, reqparse
from code.models.user import UserModel

from flask_jwt import jwt_required, current_identity



class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field can't be blank")
    parser.add_argument("password", type=str, required=True, help="This field can't be blank")

    def post(self):

        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message": "User already exists"}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()
        return {"message": "User successfully registered"}, 201