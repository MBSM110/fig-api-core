from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CoinPriceBase(BaseModel):
    price: float
    timestamp: datetime # Pydantic will validate API strings into Python datetime objects

class CoinPriceCreate(CoinPriceBase):
    coin_id: int # Used when we are inserting historical data for a specific coin

class CoinPriceResponse(CoinPriceBase):
    id: int
    coin_id: int

    model_config = {"from_attributes": True}

# Useful for your "Pattern Matching" feature: 
# Sending a list of prices back to a chart
class CoinHistoryResponse(BaseModel):
    symbol: str
    history: List[CoinPriceResponse]