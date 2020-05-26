from chalice import Chalice, CORSConfig, Response
from chalicelib.utils.database_connect import Base, engine, session
from chalicelib.service.user_service import UserService
from chalicelib.service.account_balance_service import AccountBalanceService
from chalicelib.service.account_service import AccountService
import json

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
    return Response(body=UserService().get_users(session, id),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

@app.route('/accountbalance/{account_id}', methods=['GET'])
def get_account_balance(account_id):
    return AccountBalanceService().get_account_balance(session, account_id)

@app.route('/account/{account_id}', methods=['GET'])
def get_account_details(account_id):
    return AccountService().get_account_details(session, account_id)

@app.route('/user', methods=['POST'])
def create_user():
    payload = app.current_request.json_body
    return Response(body=UserService().add_user(session, payload),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

@app.route('/account', methods=['POST'])
def create_account():
    payload = app.current_request.json_body
    return AccountService().add_account(session, payload)

    # return Response(body=AccountService().add_account(session, payload),
    #                 status_code=200,
    #                 headers={'Content-Type': 'application/json'})