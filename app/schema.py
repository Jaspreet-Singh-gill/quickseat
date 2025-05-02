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
    user_id:int
    in_out:bool
    
    
class dashboard_return(BaseModel):
    total_seats:int
    seats_not_available:int
    seats_occupied:int
    seats_available:int

class anaylytics_return(BaseModel):
    month:int
    date:int
    hour:int

    