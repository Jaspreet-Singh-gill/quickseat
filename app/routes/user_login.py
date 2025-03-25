from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import model
from .. import security
from .. import autho
router = APIRouter(tags=["user login"])

@router.post("/user_login")
def user_login(user_details:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(model.user).filter(model.user.username== user_details.username).first()
    flag = True
    if user is None:
        user = db.query(model.user).filter(model.user.email== user_details.username).first()
        if user is None:
            flag = False
        else :
            flag = True
    
    if flag == False:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "wrong credentials")
    if not security.verify_password(user_details.password,user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "wrong credentials")
    return   autho.create_token(data={"username":user.username,"user_id":user.id})

@router.delete("/user/deleteme",status_code = status.HTTP_204_NO_CONTENT)
def user_delete_me(db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    post =db.query(model.user).filter(model.user.id == user_id.id)
    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "This user does not exist")
    post.delete(synchronize_session = False)
    db.commit()