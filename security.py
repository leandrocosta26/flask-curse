from models.user import UserModel


def authentication(username, password):
    return UserModel.find_user_by_name_and_password(username, password)


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_user_by_id(user_id)
