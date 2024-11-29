from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.miner import MinerModel
from ...utils.calculations import MiningCalculator

router = APIRouter()

@router.get("/roi/{miner_id}")
async def calculate_roi(
    miner_id: int,
    electricity_cost: float = 0.12,
    uptime: float = 1.0,
    maintenance_cost: float = 0,
    db: Session = Depends(get_db)
):
    miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="Miner not found")

    calculator = MiningCalculator()
    daily_metrics = calculator.calculate_all_metrics(
        miner.hashrate,
        miner.power_consumption,
        electricity_cost,
        uptime,
        maintenance_cost,
        miner.price or 0
    )

    return {
        "miner": miner.model,
        "roi_days": daily_metrics["roi_days"],
        "daily_profit": daily_metrics["daily_profit"],
        "monthly_profit": daily_metrics["daily_profit"] * 30,
        "yearly_profit": daily_metrics["daily_profit"] * 365,
        "break_even_date": daily_metrics["break_even_date"],
        "profit_ratio": daily_metrics["profit_ratio"]
    }
