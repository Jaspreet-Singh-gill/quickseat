from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import model
from .. import schema
from .. import security
router = APIRouter()


@router.post("/admin_create")
def admin_create(new_admin:schema.admin_create,db:Session = Depends(get_db)):
    new_admin.password = security.hashpasward(new_admin.password)
    new_obj = model.adminuser(**(new_admin.dict()))
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj

@router.get("/admin/list",response_model = list[schema.admin_response])
def admin_list(db:Session = Depends(get_db)):
    admin_list = db.query(model.adminuser).all()
    return admin_list

@router.delete("/admin/{username}",status_code = status.HTTP_204_NO_CONTENT)
def admin_delete(username:str,db:Session = Depends(get_db)):
    post =db.query(model.adminuser).filter(model.adminuser.username == username).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "This admin does not exist")
    post.delete(synchronize_session = False)
    db.commit()
    



