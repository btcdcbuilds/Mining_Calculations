from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ...database.database import get_db
from ...models.miner import MinerModel

router = APIRouter()

@router.get("/depreciation/{miner_id}")
async def calculate_depreciation(
    miner_id: int,
    method: str = "straight_line",
    period_years: float = 3.5,
    db: Session = Depends(get_db)
):
    miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
    if not miner:
        raise HTTPException(status_code=404, detail="Miner not found")

    initial_value = miner.price or 0
    if initial_value == 0:
        raise HTTPException(status_code=400, detail="Miner price not set")

    age_days = (datetime.utcnow() - miner.release_date).days
    period_days = period_years * 365

    if method == "straight_line":
        daily_depreciation = initial_value / period_days
        current_value = max(0, initial_value - (daily_depreciation * age_days))
    elif method == "declining_balance":
        rate = 2 / period_years  # Double declining balance
        current_value = initial_value * ((1 - rate) ** (age_days / 365))
    else:
        raise HTTPException(status_code=400, detail="Invalid depreciation method")

    return {
        "initial_value": initial_value,
        "current_value": current_value,
        "depreciation_to_date": initial_value - current_value,
        "daily_rate": (initial_value - current_value) / age_days if age_days > 0 else 0,
        "remaining_life_days": max(0, period_days - age_days)
    }
