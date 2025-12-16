from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Common fields shared for creating and reading
class CoinBase(BaseModel):
    symbol: str
    name: str

# Schema for creating a new coin (Input validation)
class CoinCreate(CoinBase):
    pass

# Schema for reading a coin (Output formatting)
class CoinResponse(CoinBase):
    id: int
    current_price: Optional[float] = None
    created_at: datetime

    # This tells Pydantic to look at SQLAlchemy objects and 
    # extract data based on the attribute names.
    model_config = {"from_attributes": True}