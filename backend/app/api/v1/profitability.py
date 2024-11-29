from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ...database.database import get_db
from ...models.miner import MinerModel
from ...models.historical_data import HistoricalData
from ...utils.calculations import MiningCalculator

router = APIRouter()

@router.get("/profitability/{miner_id}")
async def analyze_profitability(
    miner_id: int,
    electricity_cost: float = 0.12,
    period_days: int = 30,
    include_historical: bool = True,
    db: Session = Depends(get_db)
):
    miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="Miner not found")

    calculator = MiningCalculator()

    # Get historical data
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=period_days)

    historical_data = []
    if include_historical:
        historical_data = db.query(HistoricalData)\
            .filter(HistoricalData.date >= start_date)\
            .filter(HistoricalData.date <= end_date)\
            .all()

    # Calculate metrics
    current_metrics = calculator.calculate_all_metrics(
        miner.hashrate,
        miner.power_consumption,
        electricity_cost,
        miner.price or 0
    )

    historical_metrics = []
    for data in historical_data:
        daily_metrics = calculator.calculate_historical_metrics(
            miner.hashrate,
            miner.power_consumption,
            electricity_cost,
            data.btc_price,
            data.network_difficulty,
            data.hashprice
        )
        historical_metrics.append({
            "date": data.date,
            "profit": daily_metrics["profit"],
            "revenue": daily_metrics["revenue"],
            "power_cost": daily_metrics["power_cost"]
        })

    return {
        "miner": miner.model,
        "current_metrics": current_metrics,
        "historical_metrics": historical_metrics,
        "average_daily_profit": sum(h["profit"] for h in historical_metrics) / len(historical_metrics) if historical_metrics else 0,
        "profit_trend": calculator.calculate_profit_trend(historical_metrics) if historical_metrics else None
    }
