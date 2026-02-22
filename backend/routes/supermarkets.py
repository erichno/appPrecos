from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.supermarket import Supermarket, SupermarketResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

router = APIRouter(prefix="/supermarkets", tags=["Supermarkets"])

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.get("", response_model=List[SupermarketResponse])
async def get_supermarkets(
    city_id: Optional[str] = Query(None, description="Filtrar por cidade")
):
    """Lista supermercados"""
    query = {}
    if city_id:
        query["city_id"] = city_id
    
    supermarkets = await db.supermarkets.find(query, {"_id": 0}).to_list(100)
    return [SupermarketResponse(**s) for s in supermarkets]


@router.get("/{supermarket_id}", response_model=SupermarketResponse)
async def get_supermarket(supermarket_id: str):
    """Busca supermercado por ID"""
    supermarket = await db.supermarkets.find_one({"id": supermarket_id}, {"_id": 0})
    
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    
    return SupermarketResponse(**supermarket)
