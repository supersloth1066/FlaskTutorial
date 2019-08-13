from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mysecretkey'
api = Api(app)
jwt = JWT(app, authenticate, identity)
app.config['PROPAGATE_EXCEPTIONS'] = True

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field cannot be left blank'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i : i['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i : i['name'] == name, items), None):
            return {'message': "an item with name '{}' already exists".format(name)}, 400
        req_data = Item.parser.parse_args() 
        item = {'name':name, 'price':req_data['price']}
        items.append(item)
        return {'item': item}, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message":"item deleted"}

    def put(self, name):
        req_data = Item.parser.parse_args()
        item = next(filter(lambda i : i['name'] == name, items), None)
        new_item = {'name':name, 'price':req_data['price']}
        if (item):
            item.update(new_item)
        else: 
            items.append(new_item)
        return new_item

class Items(Resource):
    def get(self):
        return {'items':items}, 200

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')

app.run(port='80', host='0.0.0.0', debug=False)