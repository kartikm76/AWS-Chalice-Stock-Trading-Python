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
        
        resource_name = STOCK_INFO_URL
        try:
            request = requests.get(resource_name+self.symbol).text
            security_data = json.loads(request)
            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = "Symbol '{0}'".format(self.symbol) + " successfully fetched"            
            self.return_payload['body'] = security_data         
        except requests.exceptions.Timeout:
            self.return_payload['status'] = FATAL_CODE
            self.return_payload['message'] = "Timeout Error {0}.".format(resource_name)            
        except requests.exceptions.TooManyRedirects:
            self.return_payload['status'] = FATAL_CODE
            self.return_payload['message'] = "Too Many Requests {0}.".format(resource_name)        
        except requests.exceptions.RequestException as e:
            self.return_payload['status'] = FATAL_CODE
            self.return_payload['message'] = "Request Format Exception {0}.".format(resource_name) 
        return self.return_payload