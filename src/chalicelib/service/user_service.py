import datetime
from chalicelib.model.user import UserORM
from chalicelib.schema.user import UserSchema
from pydantic import BaseModel, Field, ValidationError
from chalicelib.utils.object_serialize import SerializeObject

class UserService:

    return_payload = {
        "status": None,
        "user_id": None,
        "message": None
    }

    def add_user(self, session, payload):
        user = session.query(UserORM).filter(UserORM.id == payload["id"]).first()

        if not user:
            user = UserORM()
            user.id = payload["id"]
            user.name = payload["name"]
            user.ssn = payload["ssn"]
            user.isActive = "Y"
            user.profile_create_date = datetime.date.today()
            try:
                user_schema = UserSchema.from_orm(user)
                session.add(user)
                session.commit()
                self.return_payload['user_id'] = user.id
                self.return_payload['status'] = "OK"                
                self.return_payload['message'] = user.id + " successfully created"
                return self.return_payload
            except ValidationError as e:
                self.return_payload['status'] = "ERROR"
                self.return_payload['message'] = e.errors()
                return self.return_payload
        else:
            self.return_payload['user_id'] = user.id
            self.return_payload['status'] = "WARN"            
            self.return_payload['message'] = "User Exists"
            return self.return_payload
               
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

        return user_list