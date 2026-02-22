from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime, timezone
import uuid


class Location(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [latitude, longitude]


class City(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    state: str
    state_code: str
    location: Location
    population: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CityResponse(BaseModel):
    id: str
    name: str
    state: str
    state_code: str
    location: Location
    active: bool
