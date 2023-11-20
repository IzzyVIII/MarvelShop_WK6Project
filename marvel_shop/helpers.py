import decimal
import requests 
import requests_cache 
import json 

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): #if the object is a decimal we are going to encode it 
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj) #if not the JSONEncoder from json class can handle it 


   