from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..database.database import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy Model
class MinerModel(Base):
    __tablename__ = "miners"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    manufacturer = Column(String)
    hashrate = Column(Float)  # TH/s
    power_consumption = Column(Float)  # Watts
    efficiency = Column(Float)  # J/TH
    release_date = Column(DateTime)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models
class MinerBase(BaseModel):
    model: str
    manufacturer: str
    hashrate: float
    power_consumption: float
    efficiency: float
    release_date: datetime
    price: Optional[float] = None

class MinerCreate(MinerBase):
    pass

class Miner(MinerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
