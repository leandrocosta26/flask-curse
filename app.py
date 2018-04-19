import uuid
import os
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import ItemApi, ItemListApi
from resources.store import StoreApi, StoreListApi
from resources.user import UserListApi, UserApi
from security import authentication, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = str(uuid.uuid4())
api = Api(app)

print(os.environ['DATABASE_URL'])

jwt = JWT(app, authentication, identity)  # auth

api.add_resource(ItemApi, '/items/<string:name>')
api.add_resource(ItemListApi, '/items')

api.add_resource(UserListApi, '/users')
api.add_resource(UserApi, '/users/<string:username>')

api.add_resource(StoreListApi, '/stores')
api.add_resource(StoreApi, '/stores/<string:name>')

if __name__ == "__main__":
    from utils.database import db


    @app.before_first_request
    def create_tables():
        db.create_all()


    db.init_app(app)
    app.run()
