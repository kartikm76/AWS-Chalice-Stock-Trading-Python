from chalicelib.utils.db_connect import db_connect
from chalicelib.model.models import User


class UserService:
    def get_users(self, id=None):
        self.id = id
        user_list = []

        if self.id is None:
            users = User.select()
        else:
            users = User.select().where(User.id == self.id)

        for user in users:
            user_list.append({'id': user.id, 'name': user.name})
        return user_list
