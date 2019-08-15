from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='this field cannot be left blank'
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store == None:
            return {'message': '{} not found'.format(name)}, 404
        return store.json(), 200

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "an store with name '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message' : 'error inserting into database'}, 500
        return {'store': store.json()}, 201
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store == None:
            return {'message': '{} not found'.format(name)}, 404
        try:
            store.delete_from_db()
            return {'message': '{} deleted'.format(name)}, 200
        except:
            return {'message': 'error deleting store from database'}, 500


class Stores(Resource):
    def get(self):
        return {'stores': [s.json() for s in StoreModel.query.all()]}, 200