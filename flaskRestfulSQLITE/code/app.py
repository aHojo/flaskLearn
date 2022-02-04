# /c/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio/Shared/Python39_64/python.exe 
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from user import UserRegister
from item import Item, ItemList

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


api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/item/kairi
api.add_resource(ItemList, '/items') # http://localhost:5000/item/kairi
api.add_resource(UserRegister, "/register")

app.run(port=5000)