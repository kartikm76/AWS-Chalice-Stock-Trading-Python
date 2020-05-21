import datetime
import decimal

class SerializeObject():
    @classmethod
    def serialize_object(self, obj):
            self.obj = obj           

            if isinstance(self.obj, datetime.datetime):
                return self.obj.__str__()
                #return "{}-{}-{}".format(self.obj.year, self.obj.month, self.obj.day)
            
            if isinstance(self.obj, decimal.Decimal):
                return float(self.obj)
            raise TypeError