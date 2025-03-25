from pydantic import BaseModel

class admin_create(BaseModel):
    username:str
    password:str
    email:str

class admin_response(BaseModel):
    username:str
    email:str
    
    
