# /c/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio/Shared/Python39_64/python.exe 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "kairihojo"
api = Api(app)

"""
JWT creates a new endpoint called /auth
send username and password
passes it to authenticate
return jwt token

calls the identity function, gets the user id out and then we are authenticated
"""
jwt = JWT(app, authenticate, identity) 

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="this field can't be blank"
    )

    @jwt_required()
    def get(self,name):

        # for item in items:
        #     if item['name'] == name:
        #         return item

        item = next(filter(lambda x: x["name"] == name, items), None) # next gives the first item, could use list() if we wanted a list. If no items, next will give an error. None here returns None if there are no more values.

        return {"item": item}, 200 if item is not None else 404
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


api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/item/kairi
api.add_resource(ItemList, '/items') # http://localhost:5000/item/kairi

app.run(port=5000)