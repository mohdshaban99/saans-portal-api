from sqlalchemy import Column, Integer, String
from app.database import Base

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String, nullable=False)
