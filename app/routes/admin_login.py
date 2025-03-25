from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import model
from .. import security
router = APIRouter(tags=["admin login"])


@router.post("/admin_login")
def admin_login(user_details:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(model.adminuser).filter(model.adminuser.username== user_details.username).first()
    flag = True
    if user is None:
        user = db.query(model.adminuser).filter(model.adminuser.email== user_details.username).first()
        if user is None:
            flag = False
        else :
            flag = True
    
    if flag == False:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "wrong credentials")
    if not security.verify_password(user_details.password,user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "wrong credentials")
    return {"message":"Login successful"}    

    

