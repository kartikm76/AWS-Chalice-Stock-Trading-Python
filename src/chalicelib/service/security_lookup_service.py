import json
import requests
from chalicelib.utils.constants import *

class SecurityLookUpService():
    
    return_payload = {
        "status": None,
        "message": None,
        "body": None
    }

    def get_security_details(self, symbol):
        self.symbol = symbol        
        
        #resource_name = SECURITY_PRICE_URL+self.symbol+"?apikey="+API_KEY 
        try:
            #request = requests.get(resource_name).text
            request = '[{ "symbol": "MSFT", "name": "Microsoft Corporation", "price": 181.40000000 }]'
            security_data = json.loads(request)
            if security_data is not None:
                self.return_payload['status'] = SUCCESS_CODE
                self.return_payload['message'] = "Symbol '{0}'".format(self.symbol) + " successfully fetched"
                self.return_payload['body'] = security_data
            else:
                self.return_payload['status'] = ERROR_CODE
                self.return_payload['message'] = "Symbol '{0}'".format(self.symbol) + " not found"
                self.return_payload['body'] = security_data
        except requests.exceptions.Timeout:
            self.return_payload['status'] = FATAL_CODE
            self.return_payload['message'] = "Timeout Error {0}.".format(resource_name)            
        except requests.exceptions.TooManyRedirects:
            self.return_payload['status'] = FATAL_CODE
            self.return_payload['message'] = "Too Many Requests {0}.".format(resource_name)        
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return self.return_payload