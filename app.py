import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')

if __name__ == '__main__':
    from db import db # we do it here to avoid circular imports
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port='80', host='0.0.0.0', debug=False)