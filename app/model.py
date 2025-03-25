from sqlalchemy import Column, Integer, String, Float
from .database import Base
from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import TIMESTAMP
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

#True means in and False means out
class database_inout(Base):
    __tablename__ = "database_inoutput"
    id = Column(Integer, primary_key=True, nullable= False)
    current_status = Column(Boolean,nullable=
                            False)
    time = Column(TIMESTAMP(timezone=False), default=datetime.now(),nullable=False)
    user_id = Column(Integer,nullable=False)

class total_seats(Base):
    __tablename__ = "total_seats"
    id = Column(Integer, primary_key=True, nullable= False)
    total_seats = Column(Integer,nullable=False)
    total_seats_occupied = Column(Integer,nullable=False)
    time = Column(String, default=datetime.now(),nullable=False)






    
