from fastapi import APIRouter, HTTPException
from typing import List
from ...models.miner import Miner, MinerCreate

router = APIRouter()

# Temporary storage (will be replaced with database later)
miners_db = []

@router.get("/miners/", response_model=List[Miner])
async def get_miners():
    return miners_db

@router.post("/miners/", response_model=Miner)
async def create_miner(miner: MinerCreate):
    new_miner = Miner(
        id=len(miners_db) + 1,
        **miner.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    miners_db.append(new_miner)
    return new_miner
