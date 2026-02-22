from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.user import User
from models.alert import Alert, AlertCreate, AlertResponse
from routes.auth import get_current_user
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os

router = APIRouter(prefix="/users/me", tags=["User"])

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


# ========== FAVORITOS ==========

@router.get("/favorites")
async def get_favorites(current_user: User = Depends(get_current_user)):
    """Retorna favoritos do usuário"""
    # Buscar produtos favoritos
    product_favorites = []
    if current_user.favorites.get("products"):
        products = await db.products.find(
            {"id": {"$in": current_user.favorites["products"]}},
            {"_id": 0}
        ).to_list(100)
        
        # Adicionar melhor preço de cada produto
        for product in products:
            best_offer = await db.offers.find_one(
                {"product_id": product["id"]},
                {"_id": 0}
            ).sort("price", 1)
            
            if best_offer:
                product["current_price"] = best_offer["price"]
            
            product_favorites.append(product)
    
    # Buscar supermercados favoritos
    supermarket_favorites = []
    if current_user.favorites.get("supermarkets"):
        supermarkets = await db.supermarkets.find(
            {"id": {"$in": current_user.favorites["supermarkets"]}},
            {"_id": 0}
        ).to_list(100)
        supermarket_favorites = supermarkets
    
    return {
        "products": product_favorites,
        "supermarkets": supermarket_favorites
    }


@router.post("/favorites")
async def add_favorite(
    entity_type: str,  # "product" ou "supermarket"
    entity_id: str,
    current_user: User = Depends(get_current_user)
):
    """Adiciona item aos favoritos"""
    if entity_type not in ["product", "supermarket"]:
        raise HTTPException(status_code=400, detail="Invalid entity_type")
    
    field = f"favorites.{entity_type}s"
    
    # Verificar se já existe
    user_doc = await db.users.find_one(
        {"id": current_user.id, field: entity_id},
        {"_id": 0}
    )
    
    if user_doc:
        raise HTTPException(status_code=400, detail="Already in favorites")
    
    # Adicionar aos favoritos
    await db.users.update_one(
        {"id": current_user.id},
        {"$push": {field: entity_id}}
    )
    
    return {"message": "Added to favorites"}


@router.delete("/favorites/{entity_type}/{entity_id}")
async def remove_favorite(
    entity_type: str,
    entity_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove item dos favoritos"""
    if entity_type not in ["product", "supermarket"]:
        raise HTTPException(status_code=400, detail="Invalid entity_type")
    
    field = f"favorites.{entity_type}s"
    
    await db.users.update_one(
        {"id": current_user.id},
        {"$pull": {field: entity_id}}
    )
    
    return {"message": "Removed from favorites"}


# ========== ALERTAS ==========

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(current_user: User = Depends(get_current_user)):
    """Lista alertas do usuário"""
    alerts = await db.alerts.find(
        {"user_id": current_user.id, "active": True},
        {"_id": 0}
    ).to_list(100)
    
    # Enriquecer com dados do produto
    results = []
    for alert in alerts:
        product = await db.products.find_one(
            {"id": alert["product_id"]},
            {"_id": 0, "id": 1, "display_name": 1, "image_url": 1}
        )
        
        alert_response = AlertResponse(
            id=alert["id"],
            product_id=alert["product_id"],
            target_price=alert["target_price"],
            active=alert["active"],
            created_at=datetime.fromisoformat(alert["created_at"]),
            product=product
        )
        results.append(alert_response)
    
    return results


@router.post("/alerts", response_model=AlertResponse)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user)
):
    """Cria um novo alerta de preço"""
    # Verificar se produto existe
    product = await db.products.find_one({"id": alert_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Criar alerta
    alert_dict = alert_data.model_dump()
    alert_dict["user_id"] = current_user.id
    
    alert = Alert(**alert_dict)
    alert_doc = alert.model_dump()
    alert_doc["created_at"] = alert_doc["created_at"].isoformat()
    
    await db.alerts.insert_one(alert_doc)
    
    return AlertResponse(
        id=alert.id,
        product_id=alert.product_id,
        target_price=alert.target_price,
        active=alert.active,
        created_at=alert.created_at,
        product={
            "id": product["id"],
            "display_name": product["display_name"],
            "image_url": product.get("image_url")
        }
    )


@router.delete("/alerts/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """Deleta um alerta"""
    result = await db.alerts.update_one(
        {"id": alert_id, "user_id": current_user.id},
        {"$set": {"active": False}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert deleted"}
