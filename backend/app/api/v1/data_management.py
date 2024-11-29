from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...utils.data_import import DataImporter
from ...utils.validation import DataValidator
import json
import csv
from io import StringIO

router = APIRouter()

@router.post("/import/historical")
async def import_historical_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    
    if file.filename.endswith('.csv'):
        # Handle CSV file
        content_str = content.decode('utf-8')
        csv_data = list(csv.DictReader(StringIO(content_str)))
        data = csv_data
    elif file.filename.endswith('.json'):
        # Handle JSON file
        data = json.loads(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    if not DataValidator.validate_historical_data(data):
        raise HTTPException(status_code=400, detail="Invalid data format")

    try:
        imported_records = DataImporter.import_historical_data(db, data)
        return {"message": f"Successfully imported {len(imported_records)} records"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import/miners")
async def import_miners(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    
    if file.filename.endswith('.csv'):
        content_str = content.decode('utf-8')
        csv_data = list(csv.DictReader(StringIO(content_str)))
        data = csv_data
    elif file.filename.endswith('.json'):
        data = json.loads(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    if not DataValidator.validate_miner_data(data):
        raise HTTPException(status_code=400, detail="Invalid data format")

    try:
        imported_miners = DataImporter.import_miners(db, data)
        return {"message": f"Successfully imported {len(imported_miners)} miners"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
