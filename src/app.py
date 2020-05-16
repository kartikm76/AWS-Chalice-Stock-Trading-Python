from chalice import Chalice, CORSConfig, Response
from chalicelib.service.user_service import UserService

app = Chalice(app_name='stock-trading')
app.api.cors = True


@app.route('/')
def index():
    response = {"message": "Hello World!"}
    return Response(body=response,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


@app.route('/users', methods=['GET'])
def get_all_users():
    return UserService().get_users()


@app.route('/users/{id}', methods=['GET'])
def get_user(id):
    return UserService().get_users(id)