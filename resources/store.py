from models.store import StoreModel
from flask_restful import Resource
from flask_restful import reqparse

parse = reqparse.RequestParser()
parse.add_argument("name", required=True, type=str, help="This field can not be empty")


class StoreListApi(Resource):

    def post(self):
        try:
            data = parse.parse_args()
            StoreModel(data['name']).create_db()
            return {"message": "Store create!"}, 201
        except Exception as e:
            return {"message": "Erro during create store {}".format(e)}, 500

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}


class StoreApi(Resource):

    def get(self, name):
        store = StoreModel.find_one_by_name(name)
        if store:
            return {"store": store.json()}, 200
        else:
            return {"store": None}, 404

    def delete(self, name):
        store = StoreModel.find_one_by_name(name)
        if store:
            store.delete_db()
            return {'message': 'Store removed'}, 204
        else:
            return {"message": 'Store not found'}, 400
