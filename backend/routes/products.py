from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.product import Product, ProductResponse
from services.search_service import normalize_text
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta, timezone
import os

router = APIRouter(prefix="/products", tags=["Products"])

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., description="Query de busca"),
    city_id: str = Query(..., description="ID da cidade")
):
    """Busca produtos por nome"""
    normalized = normalize_text(q)
    
    # Buscar produtos que contenham a query normalizada
    products = await db.products.find({
        "$or": [
            {"canonical_name": {"$regex": normalized, "$options": "i"}},
            {"display_name": {"$regex": q, "$options": "i"}},
            {"brand": {"$regex": q, "$options": "i"}},
            {"synonyms": {"$in": [normalized]}}
        ]
    }, {"_id": 0}).limit(20).to_list(20)
    
    if not products:
        return []
    
    # Obter supermercados da cidade
    supermarkets = await db.supermarkets.find(
        {"city_id": city_id}, 
        {"_id": 0, "id": 1}
    ).to_list(100)
    supermarket_ids = [s["id"] for s in supermarkets]
    
    # Para cada produto, buscar a melhor oferta
    results = []
    for product in products:
        # Buscar melhor oferta (menor preço) nos últimos 7 dias
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        best_offer = await db.offers.find_one(
            {
                "product_id": product["id"],
                "supermarket_id": {"$in": supermarket_ids},
                "collected_at": {"$gte": seven_days_ago.isoformat()}
            },
            {"_id": 0}
        ).sort("price", 1)  # Ordenar por preço crescente
        
        if best_offer:
            # Buscar dados do supermercado
            supermarket = await db.supermarkets.find_one(
                {"id": best_offer["supermarket_id"]},
                {"_id": 0, "id": 1, "name": 1, "location": 1}
            )
            
            # Calcular horas atrás
            collected_at = datetime.fromisoformat(best_offer["collected_at"])
            hours_ago = int((datetime.now(timezone.utc) - collected_at).total_seconds() / 3600)
            
            product["best_offer"] = {
                "price": best_offer["price"],
                "is_promotion": best_offer.get("is_promotion", False),
                "hours_ago": hours_ago,
                "supermarket": {
                    "id": supermarket["id"],
                    "name": supermarket["name"],
                    "distance_km": 0  # Mock por enquanto
                }
            }
            results.append(ProductResponse(**product))
    
    return results


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Busca produto por ID"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse(**product)


@router.get("/{product_id}/history")
async def get_product_history(
    product_id: str,
    city_id: str = Query(..., description="ID da cidade"),
    days: int = Query(30, description="Número de dias de histórico")
):
    """Retorna histórico de preços do produto"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Buscar supermercados da cidade
    supermarkets = await db.supermarkets.find(
        {"city_id": city_id}, 
        {"_id": 0, "id": 1, "name": 1}
    ).to_list(100)
    supermarket_ids = [s["id"] for s in supermarkets]
    supermarket_map = {s["id"]: s["name"] for s in supermarkets}
    
    # Buscar ofertas dos últimos N dias
    since_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    offers = await db.offers.find(
        {
            "product_id": product_id,
            "supermarket_id": {"$in": supermarket_ids},
            "collected_at": {"$gte": since_date.isoformat()}
        },
        {"_id": 0}
    ).sort("collected_at", 1).to_list(1000)
    
    # Agrupar por data e supermercado
    history = []
    for offer in offers:
        history.append({
            "date": offer["collected_at"],
            "price": offer["price"],
            "supermarket_id": offer["supermarket_id"],
            "supermarket_name": supermarket_map.get(offer["supermarket_id"], "Desconhecido")
        })
    
    return {
        "product": ProductResponse(**product),
        "history": history
    }
