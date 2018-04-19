from flask_restful import Resource
from flask_restful import reqparse
from models.user import UserModel


class UserListApi(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True, help="Does not can blank")
    parse.add_argument("password", type=str, required=True, help="Does not can blank")

    def post(self):
        data = UserListApi.parse.parse_args()

        if UserModel.find_user_by_username(data["username"]) is None:
            UserModel(**data).save_user()
            return {"message": "User created"}, 201
        else:
            return {"message": "User already created"}, 400


class UserApi(Resource):

    def delete(self, username):
        user = UserModel.find_user_by_username(username)
        if user is not None:
            user.delete_user()
            return {"message": "User removed"}, 204
        else:
            return {"message": "User not found"}, 404
