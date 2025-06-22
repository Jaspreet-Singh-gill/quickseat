from jose import jwt ,JWTError
from datetime import datetime, timedelta
from . import schema

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "smallest can cast a big shadow"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_token(data:dict):
    to_incrpt = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_incrpt["exp"] = expire
    encoded_jwt = jwt.encode(to_incrpt,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":encoded_jwt,"token_type":"bearer"}

def verify_token(token:str,credentail_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentail_exceptions
        token_data = schema.TokenData(id=str(user_id))
    except JWTError:
        
        raise credentail_exceptions
    

    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentail_exceptions = HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail="Invalid Token")
    
    return verify_token(token,credentail_exceptions)