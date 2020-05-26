import json
import requests
from chalicelib.model.stock import StockORM
from chalicelib.utils.constants import *

class StockService:

    return_payload = {
        "status": None,
        "message": None        
    }

    def add_stock(self, session, payload):
        resource_name = STOCK_INFO_URL
        stock = session.query(StockORM).filter(StockORM.name == payload["symbol"]).first()

        if not stock:
            stock = StockORM()
            stock.symbol = payload["symbol"]            
            try:
                request = requests.get(resource_name+stock.symbol).text                
                stock_data = json.loads(request)
                stock.name = stock_data[0]["name"]
                session.add(stock)
                session.commit()
                self.return_payload['status'] = SUCCESS_CODE
                self.return_payload['message'] = "Stock: " + stock.symbol + " successfully added" 
            except requests.exceptions.Timeout:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Timeout Error {0}.".format(self.resource_name)
            except requests.exceptions.TooManyRedirects:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Too Many Requests {0}.".format(self.resource_name)
            except requests.exceptions.RequestException as e:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Request Format Exception {0}.".format(self.resource_name)                
        else:            
            self.return_payload['status'] = ERROR_CODE
            self.return_payload['message'] = "Stock already exists"        
        return self.return_payload
               
    def get_stocks(self, session, symbol=None):
        self.symbol = symbol
        stock_list = []
        stock_dict = {}
        
        if self.symbol is None:            
            stocks = session.query(StockORM)
        else:
            stocks = session.query(StockORM).filter(StockORM.symbol == self.symbol)

        for stock in stocks:
            stock_dict = { 'symbol': stock.symbol,
                           'name': stock.name }

            stock_list.append(stock_dict)

        return stock_list