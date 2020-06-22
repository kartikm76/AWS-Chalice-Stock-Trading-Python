import json
import requests
from chalicelib.model.security import SecurityORM
from chalicelib.utils.constants import SUCCESS_CODE, ERROR_CODE, FATAL_CODE


class SecurityService:

    return_payload = {
        "status": None,
        "message": None
    }

    def add_security(self, session, payload):
        resource_name = SECURITY_INFO_URL
        security = session.query(SecurityORM).filter(
            SecurityORM.name == payload["symbol"]).first()

        if not security:
            security = SecurityORM()
            security.symbol = payload["symbol"]
            try:
                request = requests.get(resource_name+security.symbol).text
                security_data = json.loads(request)
                security.name = security_data[0]["name"]
                session.add(security)
                session.commit()
                self.return_payload['status'] = SUCCESS_CODE
                self.return_payload['message'] = "Security: " + \
                    security.symbol + " successfully added"
            except requests.exceptions.Timeout:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Timeout Error {0}.".format(
                    self.resource_name)
            except requests.exceptions.TooManyRedirects:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Too Many Requests {0}.".format(
                    self.resource_name)
            except requests.exceptions.RequestException as e:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = "Request Format Exception {0}.".format(
                    self.resource_name)
        else:
            self.return_payload['status'] = ERROR_CODE
            self.return_payload['message'] = "Security already exists"
        return self.return_payload

    def get_securities(self, session, symbol=None):
        self.symbol = symbol
        security_list = []
        security_dict = {}

        if self.symbol is None:
            securities = session.query(SecurityORM)
        else:
            securities = session.query(SecurityORM).filter(
                SecurityORM.symbol == self.symbol)

        for security in securities:
            security_dict = {'symbol': security.symbol,
                             'name': security.name}

            security_list.append(security_dict)

        return security_list
