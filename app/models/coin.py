from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Coin(Base):
    """
    Database model representing a Cryptocurrency asset.
    """
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, index=True)
    # The ticker symbol (e.g., BTC, ETH)
    symbol = Column(String, unique=True, index=True, nullable=False)
    # The full name (e.g., Bitcoin)
    name = Column(String, nullable=False)
    # Last known price (we'll update this via the worker later)
    current_price = Column(Float, nullable=True)
    # Audit timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())