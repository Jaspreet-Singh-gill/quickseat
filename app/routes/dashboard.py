from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import model
from .. import schema
from .. import security,autho
router = APIRouter(tags=["Dasboard"])


@router.get("/dashboard")
def dashboard(db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    seats = db.query(model.total_seats).order_by(model.total_seats.time.desc()).first()
    total_seats = seats.total_seats
    seats_not_available = seats.total_seats_occupied
    
    return {"total_seats":total_seats,"seats_not_available":seats_not_available,"seats_available":seats_available}


@router.post("/dashboard/in")
def input_user(data: schema.input_person, db: Session = Depends(get_db)):
    new_person = model.database_inout(current_status=data.in_out)
    db.add(new_person)
    db.commit()
