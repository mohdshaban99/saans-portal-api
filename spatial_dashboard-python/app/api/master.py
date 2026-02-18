from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.master import Master
import pandas as pd

router = APIRouter(prefix="/master", tags=["Master"])
router = APIRouter(prefix="/states", tags=["States"])


#  csv file import data
@router.post("/import-master-data")
async def import_master_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    filename = file.filename.lower()

    # ✅ File validation
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=400, detail="Only CSV or Excel files are allowed"
        )

    # ✅ Read file
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    required_columns = {
        "FID",
        "Shape",
        "DISTRICT",
        "STATE/UT",
        "PM2.5_2017",
        "PM2.5_2018",
        "PM2.5_2019",
        "PM2.5_2020",
        "PM2.5_2021",
        "PM2.5_2022",
        "PM2.5_2023",
        "PM2.5_2024",
    }

    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "CSV columns mismatch",
                "expected": list(required_columns),
                "found": list(df.columns),
            },
        )

    # ✅ Insert data
    for _, row in df.iterrows():
        master = Master(
            fid=row["FID"],
            shape=row["Shape"],
            district=row["DISTRICT"],
            state_ut=row["STATE/UT"],
            pm25_2017=row["PM2.5_2017"],
            pm25_2018=row["PM2.5_2018"],
            pm25_2019=row["PM2.5_2019"],
            pm25_2020=row["PM2.5_2020"],
            pm25_2021=row["PM2.5_2021"],
            pm25_2022=row["PM2.5_2022"],
            pm25_2023=row["PM2.5_2023"],
            pm25_2024=row["PM2.5_2024"],
        )
        db.add(master)

    db.commit()

    return {
        "message": "CSV/Excel data imported successfully ✅",
        "rows_inserted": len(df),
    }
