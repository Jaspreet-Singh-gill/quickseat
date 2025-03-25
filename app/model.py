from sqlalchemy import Column, Integer, String, Float
from .database import Base
from datetime import datetime
class adminuser(Base):
    __tablename__ = "adminuser"

    id = Column(Integer, primary_key=True, nullable= False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(String, default=datetime.now(),nullable=False)

class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable= False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(String, default=datetime.now(),nullable=False)




    
