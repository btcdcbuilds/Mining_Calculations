from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from ..database.database import Base

class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    btc_price = Column(Float)
    network_difficulty = Column(Float)
    hashprice = Column(Float)  # USD/TH/day
    network_hashrate = Column(Float)  # EH/s
