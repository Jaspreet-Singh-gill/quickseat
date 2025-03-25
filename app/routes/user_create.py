from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import model
from .. import schema
from .. import security
router = APIRouter(tags=["user login"])

@router.post("/user_create")
def create_user(new_user:schema.user_create,db:Session = Depends(get_db)):
    new_user.password = security.hashpasward(new_user.password)
    new_obj = model.user(**(new_user.dict()))
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj
