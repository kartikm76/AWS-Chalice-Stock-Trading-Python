from chalice import Chalice, CORSConfig, Response
from chalicelib.utils.database_connect import Base, engine, session
from chalicelib.service.user_service import UserService

app = Chalice(app_name='stock-trading')
app.api.cors = True

Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    response = {"message": "Hello World!"}
    return Response(body=response,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


@app.route('/users', methods=['GET'])
def get_all_users():
    return UserService().get_users(session)

@app.route('/users/{id}', methods=['GET'])
def get_user(id):
    return UserService().get_users(session, id)