from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.master import Master
from app.models.state import State
from app.models.district import District

router = APIRouter(prefix="/particulate_matter")

# Allow only numeric years
ALLOWED_YEARS = {str(year) for year in range(2017, 2026)}


class PMRequest(BaseModel):
    state_id: int
    district_id: int
    year: str  # "2019"


@router.post("/")
def filter_data(payload: PMRequest, db: Session = Depends(get_db)):

    # Validate year (2017–2025)
    if payload.year not in ALLOWED_YEARS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid year. Allowed: {sorted(ALLOWED_YEARS)}",
        )

    # Convert to DB column name
    column_name = f"pm25_{payload.year}"

    # Extra safety check (ensures column exists in model)
    if not hasattr(Master, column_name):
        raise HTTPException(
            status_code=400,
            detail="Invalid column mapping.",
        )

    pm_column = getattr(Master, column_name)

    result = (
        db.query(
            pm_column.label("value"),
            State.state_name,
            District.district_name,
            Master.latitude,
            Master.longitude,
        )
        .join(State, State.id == Master.state_ut)
        .join(District, District.id == Master.district)
        .filter(
            Master.state_ut == payload.state_id,
            Master.district == payload.district_id,
        )
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Data not found")

    return {
        "state_id": payload.state_id,
        "state_name": result.state_name,
        "district_id": payload.district_id,
        "district_name": result.district_name,
        "latitude": result.latitude,
        "longitude": result.longitude,
        "year": payload.year,  # returns "2019"
        "value": result.value,
    }


# ============================
# 2️⃣ Year-wise Chart API
# ============================
class YearwiseRequest(BaseModel):
    state_id: int
    district_id: int


@router.post("/year-wise-chartdata")
def yearwise_chartdata(payload: YearwiseRequest, db: Session = Depends(get_db)):

    chartData = (
        db.query(Master)
        .filter(
            Master.state_ut == payload.state_id,
            Master.district == payload.district_id,
        )
        .first()
    )

    if not chartData:
        raise HTTPException(status_code=404, detail="Data not found")

    # Get district name
    district = db.query(District).filter(District.id == payload.district_id).first()
    district_name = district.district_name if district else None

    label_year = []
    label_aqi = []

    for year in sorted(ALLOWED_YEARS):
        column_name = f"pm25_{year}"

        if hasattr(chartData, column_name):
            value = getattr(chartData, column_name)

            if value is not None:
                label_year.append(year)
                label_aqi.append(value)  # keep numeric

    return {
        "district_id": chartData.district,
        "district_name": district_name,
        "label_year": label_year,
        "label_aqi": label_aqi,
    }
