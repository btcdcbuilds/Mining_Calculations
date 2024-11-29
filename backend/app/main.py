from fastapi import FastAPI, Depends, HTTPException
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
    latest_data = db.query(historical_data.HistoricalData)\
        .order_by(historical_data.HistoricalData.date.desc())\
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
