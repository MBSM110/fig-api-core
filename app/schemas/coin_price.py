from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class CoinPriceBase(BaseModel):
    price: float
    timestamp: datetime # Pydantic will validate API strings into Python datetime objects

class CoinPriceCreate(CoinPriceBase):
    pass

class CoinPriceResponse(CoinPriceBase):
    id: int
    coin_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Useful for your "Pattern Matching" feature: 
# Sending a list of prices back to a chart
class CoinHistoryResponse(BaseModel):
    symbol: str
    history: List[CoinPriceResponse]
    
    model_config = ConfigDict(from_attributes=True)