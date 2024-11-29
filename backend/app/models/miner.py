from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MinerBase(BaseModel):
    model: str
    manufacturer: str
    hashrate: float  # TH/s
    power_consumption: float  # Watts
    efficiency: float  # J/TH
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
