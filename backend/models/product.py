from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    canonical_name: str  # "leite integral itambe 1000ml"
    display_name: str    # "Leite Integral Itambé 1L"
    category: str
    subcategory: Optional[str] = None
    brand: str
    size: str
    unit: str  # "litro", "kg", "unidade"
    ean: Optional[str] = None
    image_url: Optional[str] = None
    synonyms: List[str] = Field(default_factory=list)
    variants: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductCreate(BaseModel):
    canonical_name: str
    display_name: str
    category: str
    subcategory: Optional[str] = None
    brand: str
    size: str
    unit: str
    ean: Optional[str] = None
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    display_name: str
    canonical_name: str
    category: str
    subcategory: Optional[str]
    brand: str
    size: str
    unit: str
    ean: Optional[str]
    image_url: Optional[str]
    best_offer: Optional[dict] = None
