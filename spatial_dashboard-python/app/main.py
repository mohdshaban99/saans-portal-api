from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import test_db_connection
from app.api.master import router as master_router
from app.api.state import router as state_router
from app.api.district import router as district_router
from app.api.particulate_matter import router as pm25_router

app = FastAPI()

# -----------------------------
# ✅ CORS CONFIG (REQUIRED)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(master_router)
app.include_router(state_router)
app.include_router(district_router)
app.include_router(pm25_router)


# -----------------------------
# HEALTH CHECKS
# -----------------------------
@app.get("/")
def root():
    return {"status": "Server is running 🚀"}


@app.get("/db-check")
def db_check():
    result = test_db_connection()
    if result is True:
        return {"database": "Connected successfully ✅"}
    return {"database": "Connection failed ❌", "error": result}
