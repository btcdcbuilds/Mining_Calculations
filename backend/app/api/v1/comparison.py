from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.miner import MinerModel
from ...utils.calculations import MiningCalculator

router = APIRouter()

@router.get("/compare/")
async def compare_miners(
    miner_ids: List[int],
    electricity_cost: float = 0.12,
    uptime: float = 1.0,
    db: Session = Depends(get_db)
):
    calculator = MiningCalculator()
    results = []

    for miner_id in miner_ids:
        miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
        if not miner:
            raise HTTPException(status_code=404, detail=f"Miner {miner_id} not found")

        metrics = calculator.calculate_all_metrics(
            miner.hashrate,
            miner.power_consumption,
            electricity_cost,
            uptime,
            miner.price or 0
        )

        results.append({
            "miner": miner.model,
            "daily_profit": metrics["daily_profit"],
            "efficiency": metrics["efficiency"],
            "roi_days": metrics["roi_days"],
            "power_cost": metrics["power_cost"],
            "revenue": metrics["revenue"]
        })

    return results
