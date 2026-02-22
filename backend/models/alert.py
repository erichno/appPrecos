from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone
import uuid


class Alert(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_id: str
    city_id: Optional[str] = None
    target_price: float
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_checked: Optional[datetime] = None
    triggered_at: Optional[datetime] = None


class AlertCreate(BaseModel):
    product_id: str
    target_price: float
    city_id: Optional[str] = None


class AlertResponse(BaseModel):
    id: str
    product_id: str
    target_price: float
    active: bool
    created_at: datetime
    product: Optional[dict] = None
