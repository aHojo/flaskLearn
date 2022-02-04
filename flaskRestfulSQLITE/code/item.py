
from multiprocessing import connection
import sqlite3

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

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200
        return {"message": "Item not found"}, 404


    # @jwt_required()
    def post(self, name):
        
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name '{name}' already exists."}
        
        # data = request.get_json()
        data = Item.parser.parse_args()
        #data = request.get_json() # Don't need the content type header when force=True is on. silent=True returns none if it's not json

        item = {"name": name, "price": data['price']}
        items.append(item)
        return item, 201
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "item deleted"}

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

        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {"name": name, "price": data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items": items}
