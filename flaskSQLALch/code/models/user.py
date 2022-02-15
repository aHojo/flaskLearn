import sqlite3

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self,  username, password) -> None:
        self.username = username
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "username": self.username
        }
    # @jwt_required()
    # def get(self):
        # user = current_identity
        # then implement admin auth method
    @classmethod
    def find_by_username(cls, username):
        # conn = sqlite3.connect("data.db")
        # cursor = conn.cursor()

        # query = "SELECT * FROM users where username=?"
        # result = cursor.execute(query,(username,))
        # row = result.fetchone()

        # if row:
        #     # user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        # conn.close()
        # return user

        #cls.query = SELECT * FROM users
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # conn = sqlite3.connect("data.db")
        # cursor = conn.cursor()

        # query = "SELECT * FROM users where id=?"
        # result = cursor.execute(query,(_id,))
        # row = result.fetchone()

        # if row:
        #     # user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        # conn.close()
        # return user
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
