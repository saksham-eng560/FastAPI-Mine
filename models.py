from pydantic import BaseModel

class Address(BaseModel):
    pincode:int
    city:str

class UserStructure(BaseModel):
    firstname : str
    age : int
    gender : str 
    address:Address
    
#nested models


