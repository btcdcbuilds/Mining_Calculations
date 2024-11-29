from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ...database.database import get_db
from ...models.historical_data import HistoricalData

router = APIRouter()

@router.get("/historical/")
async def get_historical_data(db: Session = Depends(get_db)):
    return db.query(HistoricalData).all()

@router.get("/historical/latest")
async def get_latest_data(db: Session = Depends(get_db)):
    latest = db.query(HistoricalData).order_by(HistoricalData.date.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No historical data found")
    return latest
