from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime, timezone
import uuid


class Address(BaseModel):
    street: str
    neighborhood: str
    zip_code: str
    city: str
    state: str


class Location(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [latitude, longitude]


class Contact(BaseModel):
    phone: Optional[str] = None
    website: Optional[str] = None
    social: Optional[Dict[str, str]] = None


class Supermarket(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    chain: Optional[str] = None
    city_id: str
    address: Address
    location: Location
    contact: Optional[Contact] = None
    opening_hours: Optional[Dict[str, str]] = None
    rating: float = 0.0
    total_reviews: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SupermarketResponse(BaseModel):
    id: str
    name: str
    chain: Optional[str]
    address: Address
    location: Location
    contact: Optional[Contact]
    opening_hours: Optional[Dict[str, str]]
    rating: float
    total_reviews: int
    distance_km: Optional[float] = None


from typing import List
