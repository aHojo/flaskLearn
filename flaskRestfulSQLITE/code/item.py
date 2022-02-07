
import sqlite3
from tkinter.messagebox import RETRY

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="this field can't be blank"
    )

    # @jwt_required()
    def get(self,name):

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return {"item": {"name": row[0], "price": row[1]}}, 200
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}
        

    # @jwt_required()
    def post(self, name):

        # if next(filter(lambda x: x["name"] == name, items), None) is not None:
        #     return {"message": f"An item with name '{name}' already exists."}, 400
        if self.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists."}, 400

        # data = request.get_json()
        data = Item.parser.parse_args()
        #data = request.get_json() # Don't need the content type header when force=True is on. silent=True returns none if it's not json

        item = {"name": name, "price": data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting an item"}, 500

        # items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect("data.db")
        connection.cursor()

        query = "DELETE from items WHERE name=?"
        connection.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': "item deleted"}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        connection.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()

    # @jwt_required()
    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type=float,
        #     required=True,
        #     help="this field can't be blank"
        # )

        # data = request.get_json()
        data = Item.parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item"}, 500

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        connection.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        connection.cursor()

        query = "SELECT * from items"
        result = connection.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})
        connection.close()

        return {"items": items}
