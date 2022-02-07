from multiprocessing import connection
import sqlite3

from flask_restful import Resource, reqparse

from flask_jwt import jwt_required, current_identity

class User: 
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @jwt_required()
    def get(self):
        user = current_identity
        # then implement admin auth method
    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        query = "SELECT * FROM users where username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()

        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()

        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field can't be blank")
    parser.add_argument("password", type=str, required=True, help="This field can't be blank")

    def post(self):

        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        user = User.find_by_username(data["username"])
        if user:
            return {"message": "User already exists"}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()
        return {"message": "User successfully registered"}, 201