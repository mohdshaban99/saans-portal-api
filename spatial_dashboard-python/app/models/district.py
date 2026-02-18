from sqlalchemy import Column, Integer, String
from app.database import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String, nullable=False)
    state_id = Column(Integer, index=True)
