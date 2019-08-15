from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field cannot be left blank'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='every item needs a store'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message' : 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "an item with name '{}' already exists".format(name)}, 400
        req_data = Item.parser.parse_args() 
        item = ItemModel(name, **req_data)
        try:
            item.save_to_db()
        except:
            return {'message' : 'error inserting into {} database with args {}'.format(name, req_data)}, 500
        return {'item': item.json()}, 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted'}
        else:
            return {'message': 'no such item found'}, 400

    def put(self, name):
        req_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if (item):
            item.price = req_data['price']
            item.save_to_db()
            return item.json(), 200
        else: 
            item = ItemModel(name, **req_data)
            item.save_to_db()
            return item.json(), 201


class Items(Resource):
    def get(self):
        return {'items': [i.json() for i in ItemModel.query.all()]}, 200