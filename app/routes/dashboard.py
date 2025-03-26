from fastapi import APIRouter
from .. database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import model
from .. import schema
from .. import security,autho
router = APIRouter(tags=["Dasboard"])


@router.get("/dashboard",response_model=schema.dashboard_return)
def dashboard(db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    seats = db.query(model.total_seats).order_by(model.total_seats.time.desc()).first()
    total_seats = seats.total_seats
    seats_not_available = seats.total_seats_occupied
    bigu = db.query(model.database_inout).filter(model.database_inout.time >="2025-03-25 08:30:00.000000").order_by(model.database_inout.user_id.desc()).all()
    smallu = db.query(model.database_inout).filter(model.database_inout.time >="2025-03-25 08:30:00.000000").order_by(model.database_inout.user_id).all()
    
    seats_sum = 0
    for i in range(smallu[0].user_id,bigu[0].user_id+1):
        value = db.query(model.database_inout).filter(model.database_inout.user_id == i).count()
        if(value%2 != 0):
            seats_sum += 1

    seats_available = total_seats - seats_sum-seats_not_available
    return {"total_seats":total_seats,"seats_not_available":seats_not_available,"seats_occupied":seats_sum,"seats_available":seats_available}
    
   # return {"total_seats":total_seats,"seats_not_available":seats_not_available,"seats_available":seats_available}


@router.post("/dashboard/in")
def input_user(data: schema.input_person, db: Session = Depends(get_db)):
    new_person = model.database_inout(current_status=data.in_out,user_id=data.user_id)
    db.add(new_person)
    db.commit()



@router.post("/dashboard/get")                                            
def input_user(data:schema.input_person, db: Session = Depends(get_db)):
  new_person = (
        db.query(model.database_inout)
        .filter(model.database_inout.user_id == data.user_id)
        .order_by(model.database_inout.time.desc())
        .first()
    )
  if new_person is None:
        return {"status": "not found"}  # Handle case when no record exists
  
  return {"status": new_person.current_status}

@router.post("/anaytics")
def anaytics(data:schema.anaylytics_return,db:Session = Depends(get_db),user_id:int = Depends(autho.get_current_user)):
    HOUR_1 = data.hour
    HOUR_2 = data.hour + 1
    day =data.date
    start_date = f"2025-03-{str(day)} {str(HOUR_1)}:00:00"
    end_date = f"2025-03-{str(day)} {str(HOUR_2)}:00:00"

    #post = db.query(model.database_inout).filter(model.database_inout.time >= start_date,model.database_inout.time <= end_date).all()
    smallu = db.query(model.database_inout).filter(model.database_inout.time >= start_date,model.database_inout.time <= end_date).order_by(model.database_inout.user_id).all()
    bigu = db.query(model.database_inout).filter(model.database_inout.time >= start_date,model.database_inout.time <= end_date).order_by(model.database_inout.user_id.desc()).all()
    seats_sum = 0
    if not smallu or not bigu:
        return {"error": "No data found for the given date and hour"}
    for i in range(smallu[0].user_id,bigu[0].user_id+1):
        value = db.query(model.database_inout).filter(model.database_inout.user_id == i).count()
        if(value%2 != 0):
            seats_sum += 1
    return{"seats available":seats_sum}