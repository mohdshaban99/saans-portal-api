from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.district import District

router = APIRouter(prefix="/districts", tags=["Districts"])

# Pydantic model for the request body
class StateRequest(BaseModel):
    state_id: int

@router.post("/")
def get_districts_by_state(
    payload: StateRequest,
    db: Session = Depends(get_db)
):
    state_id = payload.state_id

    districts = (
        db.query(District)
        .filter(District.state_id == state_id)
        .order_by(District.district_name)
        .all()
    )

    if not districts:
        return []

    return [
            {"id": d.id, "name": d.district_name}
            for d in districts
        ]
    
