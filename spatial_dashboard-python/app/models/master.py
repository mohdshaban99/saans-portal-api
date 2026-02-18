from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Master(Base):
    __tablename__ = "saas_master"

    id = Column(Integer, primary_key=True, index=True)

    fid = Column(Integer, index=True)
    shape = Column(String(100))
    state_ut = Column(Integer, index=True)
    district = Column(Integer, index=True)
    longitude = Column(Float)
    latitude = Column(Float)

    pm25_2017 = Column(Float)
    pm25_2018 = Column(Float)
    pm25_2019 = Column(Float)
    pm25_2020 = Column(Float)
    pm25_2021 = Column(Float)
    pm25_2022 = Column(Float)
    pm25_2023 = Column(Float)
    pm25_2024 = Column(Float)
    pm25_2025 = Column(Float)
    pm25_2026 = Column(Float)
