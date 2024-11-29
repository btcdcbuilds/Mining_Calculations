# setup_files.py

import os

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

# File contents
database_content = '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./mining_calculations.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

miner_model_content = '''from sqlalchemy import Column, Integer, String, Float, Date
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
'''

historical_data_content = '''from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from ..database.database import Base

class HistoricalData(Base):
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    btc_price = Column(Float)
    network_difficulty = Column(Float)
    hashprice = Column(Float)  # USD/TH/day
    network_hashrate = Column(Float)  # EH/s
'''

calculations_content = '''from datetime import datetime, date
from typing import Dict, List

class MiningCalculator:
    @staticmethod
    def calculate_daily_revenue(
        hashrate: float,  # TH/s
        hashprice: float  # USD/TH/day
    ) -> float:
        """Calculate daily revenue in USD"""
        return hashrate * hashprice

    @staticmethod
    def calculate_daily_power_cost(
        power_consumption: float,  # Watts
        electricity_cost: float,  # USD/kWh
        uptime: float = 1.0  # 0-1
    ) -> float:
        """Calculate daily power cost in USD"""
        daily_kwh = (power_consumption * 24 * uptime) / 1000
        return daily_kwh * electricity_cost

    @staticmethod
    def calculate_daily_profit(
        daily_revenue: float,
        daily_power_cost: float,
        maintenance_cost: float = 0
    ) -> float:
        """Calculate daily profit in USD"""
        return daily_revenue - daily_power_cost - maintenance_cost

    @staticmethod
    def calculate_roi_days(
        initial_investment: float,
        daily_profit: float
    ) -> float:
        """Calculate ROI period in days"""
        if daily_profit <= 0:
            return float('inf')
        return initial_investment / daily_profit

    @staticmethod
    def calculate_efficiency_ratio(
        hashrate: float,  # TH/s
        power_consumption: float  # Watts
    ) -> float:
        """Calculate efficiency in J/TH"""
        return power_consumption / hashrate

    @staticmethod
    def calculate_btc_per_day(
        hashrate: float,  # TH/s
        network_difficulty: float,
        block_reward: float = 6.25
    ) -> float:
        """Calculate expected BTC mined per day"""
        blocks_per_day = 144  # Average number of blocks per day
        network_hashrate = network_difficulty * 2**32 / 600  # H/s
        daily_btc = (hashrate * 10**12 * block_reward * blocks_per_day) / network_hashrate
        return daily_btc
'''

main_content = '''from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .database.database import engine, get_db
from .models import miner, historical_data
from .utils.calculations import MiningCalculator

# Create database tables
miner.Base.metadata.create_all(bind=engine)
historical_data.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mining Calculations API")

@app.get("/")
async def root():
    return {"message": "Mining Calculations API"}

@app.get("/miners/")
async def get_miners(db: Session = Depends(get_db)):
    miners = db.query(miner.Miner).all()
    return miners

@app.get("/calculate/daily/{miner_id}")
async def calculate_daily_metrics(
    miner_id: int,
    electricity_cost: float = 0.12,
    uptime: float = 1.0,
    db: Session = Depends(get_db)
):
    miner_data = db.query(miner.Miner).filter(miner.Miner.id == miner_id).first()
    if not miner_data:
        raise HTTPException(status_code=404, detail="Miner not found")

    # Get latest historical data
    latest_data = db.query(historical_data.HistoricalData)\\
        .order_by(historical_data.HistoricalData.date.desc())\\
        .first()

    calculator = MiningCalculator()

    daily_revenue = calculator.calculate_daily_revenue(
        miner_data.hashrate,
        latest_data.hashprice
    )

    daily_power_cost = calculator.calculate_daily_power_cost(
        miner_data.power_consumption,
        electricity_cost,
        uptime
    )

    daily_profit = calculator.calculate_daily_profit(
        daily_revenue,
        daily_power_cost
    )

    btc_per_day = calculator.calculate_btc_per_day(
        miner_data.hashrate,
        latest_data.network_difficulty
    )

    return {
        "miner": miner_data.model,
        "daily_revenue_usd": daily_revenue,
        "daily_power_cost_usd": daily_power_cost,
        "daily_profit_usd": daily_profit,
        "btc_per_day": btc_per_day,
        "efficiency_j_th": calculator.calculate_efficiency_ratio(
            miner_data.hashrate,
            miner_data.power_consumption
        )
    }
'''

def create_files():
    # Create directories if they don't exist
    directories = [
        'backend/app/models',
        'backend/app/schemas',
        'backend/app/database',
        'backend/app/utils'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        with open(f"{directory}/__init__.py", 'w') as f:
            pass

    # Write files
    write_file('backend/app/database/database.py', database_content)
    write_file('backend/app/models/miner.py', miner_model_content)
    write_file('backend/app/models/historical_data.py', historical_data_content)
    write_file('backend/app/utils/calculations.py', calculations_content)
    write_file('backend/app/main.py', main_content)

if __name__ == "__main__":
    create_files()
    print("All files created successfully!")