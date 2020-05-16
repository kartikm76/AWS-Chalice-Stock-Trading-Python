from chalicelib.model.user import User

class UserService:
    def get_users(self, session, id=None):
        self.id = id
        user_list = []
        
        if self.id is None:            
            users = session.query(User)
        else:            
            users = session.query(User).filter(User.id == self.id)

        for user in users:            
            user_list.append({'id': user.id, 'name': user.name})
        return user_list