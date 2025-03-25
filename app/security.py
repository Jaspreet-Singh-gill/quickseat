from passlib.context import CryptContext
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
def hashpasward(passward:str):
    hashed_passward = pwd_context.hash(passward)
    return hashed_passward

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)