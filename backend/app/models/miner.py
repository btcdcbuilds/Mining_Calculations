from sqlalchemy import Column, Integer, String, Float, Date
from ..database.database import Base

class Miner(Base):
    __tablename__ = "miners"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    manufacturer = Column(String)
    hashrate = Column(Float)  # TH/s
    power_consumption = Column(Float)  # Watts
    efficiency = Column(Float)  # J/TH
    release_date = Column(Date)
    price = Column(Float)
    status = Column(String)  # active/discontinued
