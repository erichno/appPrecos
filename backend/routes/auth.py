from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.user import UserCreate, UserLogin, User, UserResponse, TokenResponse
from services.auth_service import get_password_hash, verify_password, create_access_token, decode_token
from motor.motor_asyncio import AsyncIOMotorClient
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Database
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Dependency para obter usuário autenticado"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user_doc = await db.users.find_one({"id": user_id}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user_doc)


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Registra um novo usuário"""
    # Verificar se email já existe
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Criar usuário
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict["password_hash"] = get_password_hash(user_data.password)
    
    user = User(**user_dict)
    user_doc = user.model_dump()
    user_doc["created_at"] = user_doc["created_at"].isoformat()
    
    await db.users.insert_one(user_doc)
    
    # Criar token
    access_token = create_access_token({"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(**user.model_dump())
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Faz login de um usuário"""
    user_doc = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = User(**user_doc)
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Criar token
    access_token = create_access_token({"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(**user.model_dump())
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna dados do usuário autenticado"""
    return UserResponse(**current_user.model_dump())
