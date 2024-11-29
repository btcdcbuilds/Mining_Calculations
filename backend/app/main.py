from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import miners, historical_data
from .database.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mining Calculations API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(miners.router, prefix="/api/v1")
app.include_router(historical_data.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Mining Calculations API"}
