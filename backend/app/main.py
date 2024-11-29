from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import miners

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

@app.get("/")
async def root():
    return {"message": "Mining Calculations API"}
