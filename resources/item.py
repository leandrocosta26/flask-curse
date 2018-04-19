from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=False, help="This field cannot be left black!")
parser.add_argument('price', type=float, required=True, help="This field cannot be left black!")
parser.add_argument('store_id', type=int, required=True, help="This field cannot be left black!")


class ItemApi(Resource):

    @jwt_required()
    def get(self, name):
        result = ItemModel.find_one_by_name(name)
        return {"item": result.json()}, 200 if result is not None else 404

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_one_by_name(name)
        item.delete_db()
        return {"message": "item {}!".format("removed" if item else "not found")}, 204 if item else 404

    @jwt_required()
    def put(self, name):
        item = ItemModel.find_one_by_name(name)
        data = parser.parse_args()
        if item is None:
            amount = ItemModel(**data).create_db()
            return {"message": "Item created"}, 201 if amount else 400
        else:
            item.name = name
            item.price = data['price']
            item.create_db()
            return {"message": "Item updated"}, 202 if item else 400


class ItemListApi(Resource):

    @jwt_required()
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}

    @jwt_required()
    def post(self):
        data = parser.parse_args()
        try:
            ItemModel(**data).create_db()
            return {"message": "Item created"}, 201
        except Exception as e:
            return {"message": "Erro during create item {}".format(e)}, 500
