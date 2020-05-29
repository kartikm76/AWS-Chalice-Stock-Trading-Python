import datetime
from chalicelib.model.user import UserORM
from chalicelib.schema.user import UserSchema
from pydantic import BaseModel, Field, ValidationError
from chalicelib.utils.object_serialize import SerializeObject
from chalicelib.utils.constants import SUCCESS_CODE, ERROR_CODE, FATAL_CODE

class UserService:

    return_payload = {
        "status": None,
        "message": None        
    }

    def add_user(self, session, payload):
        try:
            user_schema = UserSchema.parse_obj(payload)
            print ("User Schema: ", user_schema)
            user = session.query(UserORM).filter(UserORM.id == payload["id"]).first()
            if not user:
                user = UserORM()
                user.id = payload["id"]
                user.name = payload["name"]
                user.ssn = payload["ssn"]
                user.is_active = YES_CODE
                user.profile_create_date = datetime.date.today()
            
                session.add(user)
                session.commit()
                self.return_payload['status'] = SUCCESS_CODE
                self.return_payload['message'] = user.id + " successfully created"
            else:
                self.return_payload['status'] = ERROR_CODE
                self.return_payload['message'] = "User with id: ('{0}')".format(user.id) + " already exists"
        except ValidationError as e:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = e.errors()                
        
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
                          'is_active': user.is_active,                          
                          'profile_create_date': SerializeObject.serialize_object(user.profile_create_date)}

            user_list.append(user_dict)

        return user_list