from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ...database.database import get_db
from ...models.historical_data import HistoricalData
import numpy as np
from scipy import stats

router = APIRouter()

@router.get("/network/trends")
async def get_network_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    historical = db.query(HistoricalData)\
        .filter(HistoricalData.date >= start_date)\
        .filter(HistoricalData.date <= end_date)\
        .all()

    if not historical:
        raise HTTPException(status_code=404, detail="No historical data found")

    difficulties = [h.network_difficulty for h in historical]
    hashrates = [h.network_hashrate for h in historical]
    dates = [h.date for h in historical]

    # Calculate trends
    difficulty_slope = stats.linregress(range(len(difficulties)), difficulties).slope
    hashrate_slope = stats.linregress(range(len(hashrates)), hashrates).slope

    return {
        "difficulty_trend": {
            "current": difficulties[-1],
            "change_rate": difficulty_slope,
            "prediction_next": difficulties[-1] + difficulty_slope * 14  # 14 days forecast
        },
        "hashrate_trend": {
            "current": hashrates[-1],
            "change_rate": hashrate_slope,
            "prediction_next": hashrates[-1] + hashrate_slope * 14
        },
        "correlation": np.corrcoef(difficulties, hashrates)[0,1]
    }
