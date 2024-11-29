from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from ...database.database import get_db
from ...models.historical_data import HistoricalData

router = APIRouter()

@router.get("/historical/")
async def get_historical_data(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(HistoricalData)
    if start_date:
        query = query.filter(HistoricalData.date >= start_date)
    if end_date:
        query = query.filter(HistoricalData.date <= end_date)
    return query.all()

@router.get("/historical/latest")
async def get_latest_data(db: Session = Depends(get_db)):
    latest = db.query(HistoricalData).order_by(HistoricalData.date.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No historical data found")
    return latest

@router.get("/historical/metrics")
async def get_historical_metrics(db: Session = Depends(get_db)):
    """Get min, max, and average values for key metrics"""
    result = db.query(
        func.min(HistoricalData.btc_price).label("min_btc_price"),
        func.max(HistoricalData.btc_price).label("max_btc_price"),
        func.avg(HistoricalData.btc_price).label("avg_btc_price"),
        func.min(HistoricalData.hashprice).label("min_hashprice"),
        func.max(HistoricalData.hashprice).label("max_hashprice"),
        func.avg(HistoricalData.hashprice).label("avg_hashprice")
    ).first()

    return {
        "btc_price": {
            "min": result.min_btc_price,
            "max": result.max_btc_price,
            "avg": result.avg_btc_price
        },
        "hashprice": {
            "min": result.min_hashprice,
            "max": result.max_hashprice,
            "avg": result.avg_hashprice
        }
    }
