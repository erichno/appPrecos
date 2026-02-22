from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone, timedelta
import uuid


class OfferMetadata(BaseModel):
    user_id: Optional[str] = None
    photo_url: Optional[str] = None
    ocr_verified: bool = False


class Offer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    supermarket_id: str
    price: float
    unit_price: float  # Preço por unidade base
    currency: str = "BRL"
    source: str = "crowdsourced"  # crowdsourced | scraping | api
    confidence_score: float = 0.95
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=7))
    is_promotion: bool = False
    stock_status: str = "available"  # available | low | out_of_stock
    metadata: Optional[OfferMetadata] = None


class OfferCreate(BaseModel):
    product_id: str
    supermarket_id: str
    price: float
    photo_url: Optional[str] = None
    is_promotion: bool = False


class OfferResponse(BaseModel):
    id: str
    product_id: str
    supermarket_id: str
    price: float
    collected_at: datetime
    hours_ago: Optional[int] = None
    is_promotion: bool
    stock_status: str
    supermarket: Optional[dict] = None
