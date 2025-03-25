from pydantic import BaseModel
from typing import Optional

class admin_create(BaseModel):
    username:str
    password:str
    email:str

class admin_response(BaseModel):
    username:str
    email:str

class user_create(BaseModel):
    username:str
    password:str
    email:str    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

class admin_power(BaseModel):
    total_seats:int
    total_seats_occupied:int

class input_person(BaseModel):
    in_out:bool
    
    
