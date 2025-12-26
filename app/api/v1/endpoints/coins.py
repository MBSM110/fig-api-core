from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db 
from app.models.coin import Coin
from app.models.coin_price import CoinPrice
from app.schemas.coin import CoinCreate, CoinResponse
from app.schemas.coin_price import CoinPriceCreate, CoinPriceResponse

router = APIRouter()

@router.get("/", response_model=List[CoinResponse])
async def list_coins(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coin))
    return result.scalars().all()

@router.post("/", response_model=CoinResponse)
async def create_coin(coin_in: CoinCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coin).where(Coin.symbol == coin_in.symbol.upper()))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Coin symbol already exists")

    new_coin = Coin(symbol=coin_in.symbol.upper(), name=coin_in.name)
    db.add(new_coin)
    await db.commit()
    await db.refresh(new_coin)
    return new_coin

@router.post("/{coin_id}/prices/bulk", 
             response_model=List[CoinPriceResponse])
async def upload_bulk_prices(
    coin_id: int, 
    prices_in: List[CoinPriceCreate], 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Coin).where(Coin.id == coin_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Coin not found")

    new_price_records = [
        CoinPrice(coin_id=coin_id, price=p.price, timestamp=p.timestamp) 
        for p in prices_in
    ]
    db.add_all(new_price_records)
    
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error")
    
    return new_price_records