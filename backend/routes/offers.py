from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.offer import Offer, OfferCreate, OfferResponse
from models.user import User
from routes.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import os

router = APIRouter(prefix="/offers", tags=["Offers"])

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.get("", response_model=List[OfferResponse])
async def get_offers(
    product_id: str = Query(..., description="ID do produto"),
    city_id: str = Query(..., description="ID da cidade")
):
    """Lista ofertas de um produto em uma cidade"""
    # Buscar supermercados da cidade
    supermarkets = await db.supermarkets.find(
        {"city_id": city_id}, 
        {"_id": 0}
    ).to_list(100)
    supermarket_ids = [s["id"] for s in supermarkets]
    supermarket_map = {s["id"]: s for s in supermarkets}
    
    # Buscar ofertas recentes (últimos 7 dias)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    
    offers = await db.offers.find(
        {
            "product_id": product_id,
            "supermarket_id": {"$in": supermarket_ids},
            "collected_at": {"$gte": seven_days_ago.isoformat()}
        },
        {"_id": 0}
    ).sort("price", 1).to_list(100)
    
    # Enriquecer com dados do supermercado
    results = []
    for offer in offers:
        collected_at = datetime.fromisoformat(offer["collected_at"])
        hours_ago = int((datetime.now(timezone.utc) - collected_at).total_seconds() / 3600)
        
        supermarket = supermarket_map.get(offer["supermarket_id"])
        
        offer_response = OfferResponse(
            id=offer["id"],
            product_id=offer["product_id"],
            supermarket_id=offer["supermarket_id"],
            price=offer["price"],
            collected_at=collected_at,
            hours_ago=hours_ago,
            is_promotion=offer.get("is_promotion", False),
            stock_status=offer.get("stock_status", "available"),
            supermarket={
                "id": supermarket["id"],
                "name": supermarket["name"],
                "address": supermarket["address"],
                "distance_km": 0  # Mock por enquanto
            } if supermarket else None
        )
        results.append(offer_response)
    
    return results


@router.post("", response_model=OfferResponse)
async def create_offer(
    offer_data: OfferCreate,
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova oferta (crowdsourcing)"""
    # Verificar se produto existe
    product = await db.products.find_one({"id": offer_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Verificar se supermercado existe
    supermarket = await db.supermarkets.find_one({"id": offer_data.supermarket_id})
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    
    # Criar oferta
    offer_dict = offer_data.model_dump()
    offer_dict["unit_price"] = offer_dict["price"]  # Simplificado por enquanto
    offer_dict["source"] = "crowdsourced"
    offer_dict["metadata"] = {
        "user_id": current_user.id,
        "photo_url": offer_data.photo_url,
        "ocr_verified": False
    }
    
    offer = Offer(**offer_dict)
    offer_doc = offer.model_dump()
    offer_doc["collected_at"] = offer_doc["collected_at"].isoformat()
    offer_doc["expires_at"] = offer_doc["expires_at"].isoformat()
    
    await db.offers.insert_one(offer_doc)
    
    # Atualizar reputação do usuário (+10 pontos)
    await db.users.update_one(
        {"id": current_user.id},
        {"$inc": {"reputation_score": 10}}
    )
    
    return OfferResponse(
        id=offer.id,
        product_id=offer.product_id,
        supermarket_id=offer.supermarket_id,
        price=offer.price,
        collected_at=offer.collected_at,
        hours_ago=0,
        is_promotion=offer.is_promotion,
        stock_status=offer.stock_status
    )
