from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ...models.miner import MinerModel, Miner, MinerCreate
from ...database.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/miners/", response_model=List[Miner])
async def get_miners(db: Session = Depends(get_db)):
    return db.query(MinerModel).all()

@router.post("/miners/", response_model=Miner)
async def create_miner(miner: MinerCreate, db: Session = Depends(get_db)):
    db_miner = MinerModel(**miner.dict())
    db.add(db_miner)
    db.commit()
    db.refresh(db_miner)
    return db_miner

@router.get("/miners/{miner_id}", response_model=Miner)
async def get_miner(miner_id: int, db: Session = Depends(get_db)):
    miner = db.query(MinerModel).filter(MinerModel.id == miner_id).first()
    if miner is None:
        raise HTTPException(status_code=404, detail="Miner not found")
    return miner
