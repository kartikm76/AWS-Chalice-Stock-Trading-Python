from chalice import Chalice, CORSConfig, Response
from chalicelib.utils.database_connect import Base, engine, session
from chalicelib.service.user_service import UserService
from chalicelib.service.account_balance_service import AccountBalanceService
from chalicelib.service.account_service import AccountService
from chalicelib.service.account_holding import AccountHoldingService
from chalicelib.service.trade_service import TradeService
import json

app = Chalice(app_name='security-trading')
app.api.cors = True

Base.metadata.create_all(bind=engine)


@app.route('/')
def index():
    response = {"message": "Hello World!"}
    return Response(body=response,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


# User
@app.route('/users', methods=['GET'])
def get_all_users():
    return UserService().get_users(session)


@app.route('/users/{user_id}', methods=['GET'])
def get_user(user_id):
    return Response(body=UserService().get_users(session, user_id),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})


@app.route('/user', methods=['POST'])
def create_user():
    payload = app.current_request.json_body
    return Response(body=UserService().add_user(session, payload),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

# Account Balance Query


@app.route('/accountbalance/{account_id}', methods=['GET'])
def get_account_balance(account_id):
    return AccountBalanceService().get_account_balance(session, account_id)

# Account Balance Update


@app.route('/accountbalance', methods=['POST'])
def add_update_account_balance():
    payload = app.current_request.json_body
    return AccountBalanceService().add_update_account_balance(session, payload)

# Account


@app.route('/account/{account_id}', methods=['GET'])
def get_account_details(account_id):
    return AccountService().get_account_details(session, account_id)


@app.route('/account', methods=['POST'])
def create_account():
    payload = app.current_request.json_body
    return AccountService().add_account(session, payload)

# ## Security Master
# @app.route('/security', methods=['GET'])
# def get_all_users():
#     return SecurityService().get_securities(session)

# @app.route('/security/{symbol}', methods=['GET'])
# def get_security(symbol):
#     return SecurityService().get_securities(session, symbol)

# @app.route('/security', methods=['POST'])
# def add_security():
#     payload = app.current_request.json_body
#     return SecurityService().add_security(session, payload)


@app.route('/trade', methods=['POST'])
def security_trade():
    payload = app.current_request.json_body
    return TradeService().trade(session, payload)


@app.route('/holdings/{account_id}', methods=['GET'])
def get_account_holdings(account_id):
    return AccountHoldingService().get_account_holding(session, account_id)
