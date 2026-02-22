from fastapi import APIRouter, Query
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.city import City, CityResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

router = APIRouter(prefix="/cities", tags=["Cities"])

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.get("", response_model=List[CityResponse])
async def get_cities(
    search: Optional[str] = Query(None, description="Buscar por nome da cidade")
):
    """Lista ou busca cidades"""
    query = {"active": True}
    
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    
    cities = await db.cities.find(query, {"_id": 0}).to_list(100)
    return [CityResponse(**city) for city in cities]


@router.get("/{city_id}", response_model=CityResponse)
async def get_city(city_id: str):
    """Busca cidade por ID"""
    city = await db.cities.find_one({"id": city_id}, {"_id": 0})
    
    if not city:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="City not found")
    
    return CityResponse(**city)
