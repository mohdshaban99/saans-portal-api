from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.state import State

router = APIRouter(prefix="/states", tags=["States"])

@router.get("/")
def get_all_states(db: Session = Depends(get_db)):
    states = db.query(State).all()

    return [
        {
            "id": state.id,
            "name": state.state_name
        }
        for state in states
    ]
