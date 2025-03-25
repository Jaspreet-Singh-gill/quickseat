from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import model
from .. import schema
from .. import security
from .. import autho
router = APIRouter(tags=["admin login"])


@router.post("/admin_create")
def admin_create(new_admin:schema.admin_create,db:Session = Depends(get_db),
                 user_id:int = Depends(autho.get_current_user)):
    new_admin.password = security.hashpasward(new_admin.password)
    new_obj = model.adminuser(**(new_admin.dict()))
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj

@router.get("/admin/list",response_model = list[schema.admin_response])
def admin_list(db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    admin_list = db.query(model.adminuser).all()
    return admin_list



@router.delete("/admin/deleteme",status_code = status.HTTP_204_NO_CONTENT)
def admin_delete_me(db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    post =db.query(model.adminuser).filter(model.adminuser.id == user_id.id)
    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "This admin does not exist")
    post.delete(synchronize_session = False)
    db.commit()

@router.delete("/admin/{username}",status_code = status.HTTP_204_NO_CONTENT)
def admin_delete(username:str,db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    post =db.query(model.adminuser).filter(model.adminuser.username == username)
    if not post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "This admin does not exist")
    post.delete(synchronize_session = False)
    db.commit()
    
