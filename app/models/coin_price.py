from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class CoinPrice(Base):
    """
    Stores historical price data.
    """
    __tablename__ = "coin_prices"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("coins.id"), nullable=False, index=True)
    
    # THE FIX: 
    # This is the "Time of the Trade" from the API (e.g., Binance, Coingecko).
    # It is NOT default. You must provide it explicitly when creating the record.
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # The value of the asset at that specific timestamp
    price = Column(Float, nullable=False)
    
    # Audit trail: When did our system actually save this row?
    # This IS useful to have as a default for debugging your scripts.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    coin = relationship("Coin", backref="prices")