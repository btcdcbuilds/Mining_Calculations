from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...database.database import get_db
from ...models.miner import MinerModel
from ...models.historical_data import HistoricalData
from ...utils.calculations import MiningCalculator

router = APIRouter()

@router.get("/portfolio/summary")
async def get_portfolio_summary(
    electricity_cost: float = 0.12,
    db: Session = Depends(get_db)
):
    miners = db.query(MinerModel).all()
    latest_data = db.query(HistoricalData)\
        .order_by(HistoricalData.date.desc())\
        .first()

    calculator = MiningCalculator()
    total_hashrate = 0
    total_power = 0
    total_revenue = 0
    total_cost = 0
    total_value = 0

    miners_data = []
    for miner in miners:
        hashrate = miner.hashrate
        power = miner.power_consumption

        daily_revenue = calculator.calculate_daily_revenue(
            hashrate, latest_data.hashprice
        )
        daily_cost = calculator.calculate_daily_power_cost(
            power, electricity_cost
        )

        total_hashrate += hashrate
        total_power += power
        total_revenue += daily_revenue
        total_cost += daily_cost
        total_value += miner.price or 0

        miners_data.append({
            "miner": miner.model,
            "hashrate": hashrate,
            "daily_revenue": daily_revenue,
            "daily_cost": daily_cost,
            "efficiency": miner.efficiency
        })

    return {
        "portfolio_metrics": {
            "total_hashrate": total_hashrate,
            "total_power_consumption": total_power,
            "daily_revenue": total_revenue,
            "daily_cost": total_cost,
            "daily_profit": total_revenue - total_cost,
            "total_asset_value": total_value,
            "roi_ratio": (total_revenue - total_cost) / total_value if total_value > 0 else 0
        },
        "miners": miners_data
    }
