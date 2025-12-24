from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.config import settings
from app.core.database import get_db
from app.models.coin import Coin
from app.models.coin_price import CoinPrice
from app.schemas.coin import CoinCreate, CoinResponse
from app.schemas.coin_price import CoinPriceCreate, CoinPriceResponse

app = FastAPI(
    title="Fig API Core",
    description="Backend API for the Fig Crypto Analysis Platform",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "project": "Fig API Core"}

# --- COIN MANAGEMENT ---

@app.get("/coins/", response_model=List[CoinResponse])
async def list_coins(db: AsyncSession = Depends(get_db)):
    """
    Returns a list of all coins registered in the database.
    The worker uses this to find the correct internal ID for a coin (like XRP).
    """
    result = await db.execute(select(Coin))
    coins = result.scalars().all()
    return coins

@app.post("/coins/", response_model=CoinResponse)
async def create_coin(coin_in: CoinCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new coin (e.g., XRP, BTC) in the database.
    The worker needs this 'Parent' record to exist before it can upload prices.
    """
    # Check if coin already exists
    result = await db.execute(select(Coin).where(Coin.symbol == coin_in.symbol.upper()))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Coin symbol already exists")

    new_coin = Coin(symbol=coin_in.symbol.upper(), name=coin_in.name)
    db.add(new_coin)
    await db.commit()
    await db.refresh(new_coin)
    return new_coin

# --- BULK DATA INGESTION (For fig-worker-data) ---

@app.post("/coins/{coin_id}/prices/bulk", response_model=List[CoinPriceResponse])
async def upload_bulk_prices(
    coin_id: int, 
    prices_in: List[CoinPriceCreate], 
    db: AsyncSession = Depends(get_db)
):
    """
    The 'Door' for the worker. Takes a massive list of historical prices
    and saves them in one single transaction.
    """
    # Verify the coin exists
    result = await db.execute(select(Coin).where(Coin.id == coin_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Coin not found")

    # Create the model objects
    new_price_records = [
        CoinPrice(
            coin_id=coin_id,
            price=p.price,
            timestamp=p.timestamp
        ) for p in prices_in
    ]
    
    db.add_all(new_price_records)
    
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return new_price_records