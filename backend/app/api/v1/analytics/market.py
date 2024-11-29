from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ...database.database import get_db
from ...models.historical_data import HistoricalData
import numpy as np
from scipy import stats

router = APIRouter()

@router.get("/market/analysis")
async def analyze_market(
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

    btc_prices = [h.btc_price for h in historical]
    hashprices = [h.hashprice for h in historical]

    # Calculate volatility
    btc_volatility = np.std(btc_prices) / np.mean(btc_prices)
    hashprice_volatility = np.std(hashprices) / np.mean(hashprices)

    # Calculate trends
    btc_trend = stats.linregress(range(len(btc_prices)), btc_prices)
    hashprice_trend = stats.linregress(range(len(hashprices)), hashprices)

    # Generate alerts
    alerts = []
    if btc_trend.slope < 0:
        alerts.append("BTC price showing downward trend")
    if hashprice_trend.slope < 0:
        alerts.append("Hashprice showing downward trend")
    if btc_volatility > 0.1:  # 10% threshold
        alerts.append("High BTC price volatility detected")

    return {
        "btc_metrics": {
            "current_price": btc_prices[-1],
            "volatility": btc_volatility,
            "trend": "up" if btc_trend.slope > 0 else "down",
            "trend_strength": abs(btc_trend.rvalue)
        },
        "hashprice_metrics": {
            "current": hashprices[-1],
            "volatility": hashprice_volatility,
            "trend": "up" if hashprice_trend.slope > 0 else "down",
            "trend_strength": abs(hashprice_trend.rvalue)
        },
        "correlation": np.corrcoef(btc_prices, hashprices)[0,1],
        "alerts": alerts,
        "market_sentiment": "bullish" if btc_trend.slope > 0 and hashprice_trend.slope > 0 else "bearish"
    }
