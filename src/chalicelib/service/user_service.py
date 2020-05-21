from chalicelib.model.user import UserORM
from chalicelib.schema.user import UserSchema
from pydantic import BaseModel, Field
from chalicelib.utils.object_serialize import SerializeObject


class UserService:

    def get_users(self, session, id=None):
        self.id = id
        user_list = []
        user_dict = {}
        
        if self.id is None:            
            users = session.query(UserORM)
        else:
            users = session.query(UserORM).filter(UserORM.id == self.id)

        for user in  users:     
            user_dict = { 'id':  user.id,
                          'name': user.name,
                          'ssn': user.ssn,
                          'is_active': user.isActive,
                          'profile_create_date': SerializeObject.serialize_object(user.profile_create_date)}

            user_list.append(user_dict)

            #user_orm = UserORM(id=user.id, name=user.name, isActive=user.isActive, ssn=user.ssn)
            #user_schema = UserSchema.from_orm(user_orm)            
            #user_list.append(dict(user_schema))
        
        return user_list