from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ...database.database import get_db
from ...models.miner import MinerModel
from ...models.historical_data import HistoricalData
from ...utils.calculations import MiningCalculator

router = APIRouter()

@router.get("/cost-basis/{miner_id}")
async def calculate_cost_basis(
    miner_id: int,
    electricity_cost: float = 0.12,
    include_depreciation: bool = True,
    db: Session = Depends(get_db)
):
    miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="Miner not found")

    calculator = MiningCalculator()
    days_since_release = (datetime.utcnow() - miner.release_date).days

    # Get historical data
    historical = db.query(HistoricalData)\
        .filter(HistoricalData.date >= miner.release_date)\
        .all()

    # Calculate cumulative costs and revenue
    total_power_cost = 0
    total_revenue = 0
    total_btc_mined = 0

    for data in historical:
        daily_power_cost = calculator.calculate_daily_power_cost(
            miner.power_consumption, electricity_cost
        )
        daily_revenue = calculator.calculate_daily_revenue(
            miner.hashrate, data.hashprice
        )
        daily_btc = calculator.calculate_btc_per_day(
            miner.hashrate, data.network_difficulty
        )

        total_power_cost += daily_power_cost
        total_revenue += daily_revenue
        total_btc_mined += daily_btc

    # Include initial investment and depreciation
    initial_investment = miner.price or 0
    current_value = initial_investment
    if include_depreciation:
        depreciation_rate = initial_investment / (3.5 * 365)  # 3.5 years straight line
        total_depreciation = depreciation_rate * days_since_release
        current_value = max(0, initial_investment - total_depreciation)

    total_cost = total_power_cost + (initial_investment - current_value)

    return {
        "initial_investment": initial_investment,
        "current_value": current_value,
        "total_power_cost": total_power_cost,
        "total_revenue": total_revenue,
        "total_btc_mined": total_btc_mined,
        "cost_per_btc": total_cost / total_btc_mined if total_btc_mined > 0 else float('inf'),
        "net_profit": total_revenue - total_cost,
        "roi_percentage": ((total_revenue - total_cost) / initial_investment * 100) if initial_investment > 0 else 0
    }
