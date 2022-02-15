
import sqlite3

#https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="this field can't be blank"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    # @jwt_required()
    def get(self, name):

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return {"item": {"name": row[0], "price": row[1]}}, 200
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404


    @jwt_required(fresh=True) # needs to be a newly created jwt access_token
    def post(self, name):

        # if next(filter(lambda x: x["name"] == name, items), None) is not None:
        #     return {"message": f"An item with name '{name}' already exists."}, 400
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists."}, 400

        # data = request.get_json()
        data = Item.parser.parse_args()
        #data = request.get_json() # Don't need the content type header when force=True is on. silent=True returns none if it's not json

        # item = {"name": name, "price": data['price']}
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            # item.insert()
            item.save_to_db()
        except Exception as e:
            print(data)
            print(e)
            return {"message": "An error occurred inserting an item"}, 500

        # items.append(item)
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # connection = sqlite3.connect("data.db")
        # connection.cursor()

        # query = "DELETE from items WHERE name=?"
        # connection.execute(query, (name,))

        # connection.commit()
        # connection.close()

        # return {'message': "item deleted"}
        claims = get_jwt()

        if not claims["is_admin"]:
            return {"message": "Admin privilege required."}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "item deleted"}


    # @jwt_required
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
        item = ItemModel.find_by_name(name)
        # updated_item = {"name": name, "price": data['price']}
        # updated_item = ItemModel(name, data["price"])
        

        if item is None:
            try:
                item = ItemModel(name, data["price"])

                # ItemModel.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item"}, 500
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        # connection = sqlite3.connect("data.db")
        # connection.cursor()

        # query = "SELECT * from items"
        # result = connection.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price": row[1]})
        # connection.close()

        # return {"items": items}
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        user_id = get_jwt()
        items = list(map(lambda item: item.json(), ItemModel.find_all()))

        if user_id:
            return {'items': items},200
        return {
            "items": [item['name'] for item in items],
            "message": "more data available if you are logged in and pass your token. "
        }, 200
