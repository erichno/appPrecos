"""
Script para popular o banco de dados com dados fictícios
Executar: python -m scripts.seed_data
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import random

load_dotenv()

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]


async def seed_cities():
    """Adiciona São Paulo ao banco"""
    cities = [
        {
            "id": "city-sp-001",
            "name": "São Paulo",
            "state": "São Paulo",
            "state_code": "SP",
            "location": {
                "type": "Point",
                "coordinates": [-23.5505, -46.6333]
            },
            "population": 12300000,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Clear existing
    await db.cities.delete_many({})
    await db.cities.insert_many(cities)
    print(f"✅ {len(cities)} cidade(s) adicionada(s)")


async def seed_supermarkets():
    """Adiciona 5 supermercados em São Paulo"""
    supermarkets = [
        {
            "id": "market-001",
            "name": "Pão de Açúcar",
            "chain": "Grupo Pão de Açúcar",
            "city_id": "city-sp-001",
            "address": {
                "street": "Av. Paulista, 1000",
                "neighborhood": "Bela Vista",
                "zip_code": "01310-100",
                "city": "São Paulo",
                "state": "SP"
            },
            "location": {
                "type": "Point",
                "coordinates": [-23.5629, -46.6544]
            },
            "contact": {
                "phone": "+551130001000",
                "website": "https://www.paodeacucar.com",
                "social": {"instagram": "@paodeacucar"}
            },
            "opening_hours": {
                "monday": "07:00-23:00",
                "tuesday": "07:00-23:00",
                "wednesday": "07:00-23:00",
                "thursday": "07:00-23:00",
                "friday": "07:00-23:00",
                "saturday": "07:00-23:00",
                "sunday": "08:00-22:00"
            },
            "rating": 4.5,
            "total_reviews": 1250,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "market-002",
            "name": "Carrefour",
            "chain": "Grupo Carrefour",
            "city_id": "city-sp-001",
            "address": {
                "street": "R. da Consolação, 2525",
                "neighborhood": "Consolação",
                "zip_code": "01416-001",
                "city": "São Paulo",
                "state": "SP"
            },
            "location": {
                "type": "Point",
                "coordinates": [-23.5489, -46.6597]
            },
            "contact": {
                "phone": "+551130002000",
                "website": "https://www.carrefour.com.br"
            },
            "opening_hours": {
                "monday": "07:00-22:00",
                "tuesday": "07:00-22:00",
                "wednesday": "07:00-22:00",
                "thursday": "07:00-22:00",
                "friday": "07:00-22:00",
                "saturday": "07:00-22:00",
                "sunday": "08:00-20:00"
            },
            "rating": 4.2,
            "total_reviews": 890,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "market-003",
            "name": "Extra Hipermercado",
            "chain": "Grupo Pão de Açúcar",
            "city_id": "city-sp-001",
            "address": {
                "street": "Av. Rebouças, 3970",
                "neighborhood": "Pinheiros",
                "zip_code": "05402-600",
                "city": "São Paulo",
                "state": "SP"
            },
            "location": {
                "type": "Point",
                "coordinates": [-23.5689, -46.6845]
            },
            "contact": {
                "phone": "+551130003000",
                "website": "https://www.extra.com.br"
            },
            "opening_hours": {
                "monday": "07:00-00:00",
                "tuesday": "07:00-00:00",
                "wednesday": "07:00-00:00",
                "thursday": "07:00-00:00",
                "friday": "07:00-00:00",
                "saturday": "07:00-00:00",
                "sunday": "07:00-00:00"
            },
            "rating": 4.0,
            "total_reviews": 650,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "market-004",
            "name": "Dia Supermercado",
            "chain": "Dia%",
            "city_id": "city-sp-001",
            "address": {
                "street": "R. Augusta, 2690",
                "neighborhood": "Cerqueira César",
                "zip_code": "01412-100",
                "city": "São Paulo",
                "state": "SP"
            },
            "location": {
                "type": "Point",
                "coordinates": [-23.5610, -46.6620]
            },
            "contact": {
                "phone": "+551130004000"
            },
            "opening_hours": {
                "monday": "07:00-22:00",
                "tuesday": "07:00-22:00",
                "wednesday": "07:00-22:00",
                "thursday": "07:00-22:00",
                "friday": "07:00-22:00",
                "saturday": "07:00-22:00",
                "sunday": "07:00-22:00"
            },
            "rating": 3.8,
            "total_reviews": 420,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "market-005",
            "name": "Assaí Atacadista",
            "chain": "Grupo Pão de Açúcar",
            "city_id": "city-sp-001",
            "address": {
                "street": "Av. Inajar de Souza, 1081",
                "neighborhood": "Vila Nova Cachoeirinha",
                "zip_code": "02712-000",
                "city": "São Paulo",
                "state": "SP"
            },
            "location": {
                "type": "Point",
                "coordinates": [-23.4782, -46.6569]
            },
            "contact": {
                "phone": "+551130005000",
                "website": "https://www.assai.com.br"
            },
            "opening_hours": {
                "monday": "07:00-22:00",
                "tuesday": "07:00-22:00",
                "wednesday": "07:00-22:00",
                "thursday": "07:00-22:00",
                "friday": "07:00-22:00",
                "saturday": "07:00-22:00",
                "sunday": "07:00-21:00"
            },
            "rating": 4.3,
            "total_reviews": 980,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.supermarkets.delete_many({})
    await db.supermarkets.insert_many(supermarkets)
    print(f"✅ {len(supermarkets)} supermercado(s) adicionado(s)")


async def seed_products():
    """Adiciona 50 produtos de categorias variadas"""
    products = [
        # Laticínios (10 produtos)
        {
            "id": "prod-001",
            "canonical_name": "leite integral itambe 1000ml",
            "display_name": "Leite Integral Itambé 1L",
            "category": "laticínios",
            "subcategory": "leite",
            "brand": "Itambé",
            "size": "1000ml",
            "unit": "litro",
            "ean": "7891000100103",
            "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300",
            "synonyms": ["leite itambe 1L", "itambe integral 1000ml"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-002",
            "canonical_name": "leite desnatado parmalat 1000ml",
            "display_name": "Leite Desnatado Parmalat 1L",
            "category": "laticínios",
            "subcategory": "leite",
            "brand": "Parmalat",
            "size": "1000ml",
            "unit": "litro",
            "ean": "7891000100204",
            "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300",
            "synonyms": ["parmalat desnatado 1L"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-003",
            "canonical_name": "iogurte natural nestle 170g",
            "display_name": "Iogurte Natural Nestlé 170g",
            "category": "laticínios",
            "subcategory": "iogurte",
            "brand": "Nestlé",
            "size": "170g",
            "unit": "grama",
            "ean": "7891000100305",
            "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-004",
            "canonical_name": "queijo mussarela fatiado president 150g",
            "display_name": "Queijo Mussarela Fatiado Président 150g",
            "category": "laticínios",
            "subcategory": "queijo",
            "brand": "Président",
            "size": "150g",
            "unit": "grama",
            "ean": "7891000100406",
            "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-005",
            "canonical_name": "manteiga com sal itambe 200g",
            "display_name": "Manteiga com Sal Itambé 200g",
            "category": "laticínios",
            "subcategory": "manteiga",
            "brand": "Itambé",
            "size": "200g",
            "unit": "grama",
            "ean": "7891000100507",
            "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Grãos e cereais (10 produtos)
        {
            "id": "prod-006",
            "canonical_name": "arroz branco tipo 1 tio joao 5000g",
            "display_name": "Arroz Branco Tipo 1 Tio João 5kg",
            "category": "grãos",
            "subcategory": "arroz",
            "brand": "Tio João",
            "size": "5000g",
            "unit": "kg",
            "ean": "7891000200108",
            "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300",
            "synonyms": ["arroz tio joao 5kg"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-007",
            "canonical_name": "feijao preto camil 1000g",
            "display_name": "Feijão Preto Camil 1kg",
            "category": "grãos",
            "subcategory": "feijão",
            "brand": "Camil",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000200209",
            "image_url": "https://images.unsplash.com/photo-1583844812339-df8f62ad0b0b?w=300",
            "synonyms": ["feijao camil 1kg"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-008",
            "canonical_name": "feijao carioca kicaldo 1000g",
            "display_name": "Feijão Carioca Kicaldo 1kg",
            "category": "grãos",
            "subcategory": "feijão",
            "brand": "Kicaldo",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000200310",
            "image_url": "https://images.unsplash.com/photo-1583844812339-df8f62ad0b0b?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-009",
            "canonical_name": "macarrao espaguete barilla 500g",
            "display_name": "Macarrão Espaguete Barilla 500g",
            "category": "grãos",
            "subcategory": "massas",
            "brand": "Barilla",
            "size": "500g",
            "unit": "grama",
            "ean": "7891000200411",
            "image_url": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-010",
            "canonical_name": "farinha trigo especial dona benta 1000g",
            "display_name": "Farinha de Trigo Especial Dona Benta 1kg",
            "category": "grãos",
            "subcategory": "farinha",
            "brand": "Dona Benta",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000200512",
            "image_url": "https://images.unsplash.com/photo-1628582890995-5f844f82ee3c?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Bebidas (10 produtos)
        {
            "id": "prod-011",
            "canonical_name": "refrigerante coca-cola 2000ml",
            "display_name": "Refrigerante Coca-Cola 2L",
            "category": "bebidas",
            "subcategory": "refrigerante",
            "brand": "Coca-Cola",
            "size": "2000ml",
            "unit": "litro",
            "ean": "7891000300113",
            "image_url": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=300",
            "synonyms": ["coca 2L", "coca-cola 2 litros"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-012",
            "canonical_name": "refrigerante guarana antarctica 2000ml",
            "display_name": "Refrigerante Guaraná Antarctica 2L",
            "category": "bebidas",
            "subcategory": "refrigerante",
            "brand": "Antarctica",
            "size": "2000ml",
            "unit": "litro",
            "ean": "7891000300214",
            "image_url": "https://images.unsplash.com/photo-1625740550303-6f8dbb1e0f35?w=300",
            "synonyms": ["guarana 2L"],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-013",
            "canonical_name": "suco laranja natural valle 1000ml",
            "display_name": "Suco de Laranja Natural Del Valle 1L",
            "category": "bebidas",
            "subcategory": "suco",
            "brand": "Del Valle",
            "size": "1000ml",
            "unit": "litro",
            "ean": "7891000300315",
            "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-014",
            "canonical_name": "agua mineral crystal sem gas 1500ml",
            "display_name": "Água Mineral Crystal Sem Gás 1,5L",
            "category": "bebidas",
            "subcategory": "água",
            "brand": "Crystal",
            "size": "1500ml",
            "unit": "litro",
            "ean": "7891000300416",
            "image_url": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-015",
            "canonical_name": "cafe tradicional pilao 500g",
            "display_name": "Café Tradicional Pilão 500g",
            "category": "bebidas",
            "subcategory": "café",
            "brand": "Pilão",
            "size": "500g",
            "unit": "grama",
            "ean": "7891000300517",
            "image_url": "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Açúcar e óleo (5 produtos)
        {
            "id": "prod-016",
            "canonical_name": "acucar cristal uniao 1000g",
            "display_name": "Açúcar Cristal União 1kg",
            "category": "mercearia",
            "subcategory": "açúcar",
            "brand": "União",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000400118",
            "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-017",
            "canonical_name": "acucar refinado uniao 1000g",
            "display_name": "Açúcar Refinado União 1kg",
            "category": "mercearia",
            "subcategory": "açúcar",
            "brand": "União",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000400219",
            "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-018",
            "canonical_name": "oleo soja liza 900ml",
            "display_name": "Óleo de Soja Liza 900ml",
            "category": "mercearia",
            "subcategory": "óleo",
            "brand": "Liza",
            "size": "900ml",
            "unit": "litro",
            "ean": "7891000400320",
            "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-019",
            "canonical_name": "sal refinado cisne 1000g",
            "display_name": "Sal Refinado Cisne 1kg",
            "category": "mercearia",
            "subcategory": "temperos",
            "brand": "Cisne",
            "size": "1000g",
            "unit": "kg",
            "ean": "7891000400421",
            "image_url": "https://images.unsplash.com/photo-1495479258772-b1f4f53c2b7c?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-020",
            "canonical_name": "vinagre alcool castelo 750ml",
            "display_name": "Vinagre de Álcool Castelo 750ml",
            "category": "mercearia",
            "subcategory": "temperos",
            "brand": "Castelo",
            "size": "750ml",
            "unit": "litro",
            "ean": "7891000400522",
            "image_url": "https://images.unsplash.com/photo-1607623488025-d37e61b8e239?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Higiene e limpeza (10 produtos)
        {
            "id": "prod-021",
            "canonical_name": "papel higienico neve folha dupla 12 rolos",
            "display_name": "Papel Higiênico Neve Folha Dupla 12 Rolos",
            "category": "higiene",
            "subcategory": "papel",
            "brand": "Neve",
            "size": "12 unidades",
            "unit": "unidade",
            "ean": "7891000500123",
            "image_url": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-022",
            "canonical_name": "sabonete dove original 90g",
            "display_name": "Sabonete Dove Original 90g",
            "category": "higiene",
            "subcategory": "sabonete",
            "brand": "Dove",
            "size": "90g",
            "unit": "grama",
            "ean": "7891000500224",
            "image_url": "https://images.unsplash.com/photo-1598791318878-10e76d178023?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-023",
            "canonical_name": "shampoo clear anticaspa 400ml",
            "display_name": "Shampoo Clear Anticaspa 400ml",
            "category": "higiene",
            "subcategory": "cabelo",
            "brand": "Clear",
            "size": "400ml",
            "unit": "litro",
            "ean": "7891000500325",
            "image_url": "https://images.unsplash.com/photo-1617897903246-719242758050?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-024",
            "canonical_name": "creme dental colgate total 12 90g",
            "display_name": "Creme Dental Colgate Total 12 90g",
            "category": "higiene",
            "subcategory": "dental",
            "brand": "Colgate",
            "size": "90g",
            "unit": "grama",
            "ean": "7891000500426",
            "image_url": "https://images.unsplash.com/photo-1622372738946-62e02505feb3?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-025",
            "canonical_name": "desodorante rexona men 150ml",
            "display_name": "Desodorante Rexona Men 150ml",
            "category": "higiene",
            "subcategory": "desodorante",
            "brand": "Rexona",
            "size": "150ml",
            "unit": "litro",
            "ean": "7891000500527",
            "image_url": "https://images.unsplash.com/photo-1617897336788-48c969e88e4d?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-026",
            "canonical_name": "detergente ype neutro 500ml",
            "display_name": "Detergente Ypê Neutro 500ml",
            "category": "limpeza",
            "subcategory": "louça",
            "brand": "Ypê",
            "size": "500ml",
            "unit": "litro",
            "ean": "7891000500628",
            "image_url": "https://images.unsplash.com/photo-1563291020-4f5280f80ae0?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-027",
            "canonical_name": "agua sanitaria qboa 1000ml",
            "display_name": "Água Sanitária Q-Boa 1L",
            "category": "limpeza",
            "subcategory": "sanitário",
            "brand": "Q-Boa",
            "size": "1000ml",
            "unit": "litro",
            "ean": "7891000500729",
            "image_url": "https://images.unsplash.com/photo-1585421514738-01798e348b17?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-028",
            "canonical_name": "sabao po omo multiacao 1600g",
            "display_name": "Sabão em Pó Omo Multiação 1,6kg",
            "category": "limpeza",
            "subcategory": "roupa",
            "brand": "Omo",
            "size": "1600g",
            "unit": "kg",
            "ean": "7891000500830",
            "image_url": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-029",
            "canonical_name": "esponja limpeza scotch-brite dupla face 3 unidades",
            "display_name": "Esponja de Limpeza Scotch-Brite Dupla Face 3un",
            "category": "limpeza",
            "subcategory": "louça",
            "brand": "Scotch-Brite",
            "size": "3 unidades",
            "unit": "unidade",
            "ean": "7891000500931",
            "image_url": "https://images.unsplash.com/photo-1625245488600-f14bf4d0c00b?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-030",
            "canonical_name": "limpador multiuso veja 500ml",
            "display_name": "Limpador Multiuso Veja 500ml",
            "category": "limpeza",
            "subcategory": "multiuso",
            "brand": "Veja",
            "size": "500ml",
            "unit": "litro",
            "ean": "7891000501032",
            "image_url": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Snacks e doces (10 produtos)
        {
            "id": "prod-031",
            "canonical_name": "biscoito cream cracker club social 144g",
            "display_name": "Biscoito Cream Cracker Club Social 144g",
            "category": "snacks",
            "subcategory": "biscoito",
            "brand": "Club Social",
            "size": "144g",
            "unit": "grama",
            "ean": "7891000600133",
            "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-032",
            "canonical_name": "biscoito recheado oreo 90g",
            "display_name": "Biscoito Recheado Oreo 90g",
            "category": "snacks",
            "subcategory": "biscoito",
            "brand": "Oreo",
            "size": "90g",
            "unit": "grama",
            "ean": "7891000600234",
            "image_url": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-033",
            "canonical_name": "salgadinho doritos queijo nacho 140g",
            "display_name": "Salgadinho Doritos Queijo Nacho 140g",
            "category": "snacks",
            "subcategory": "salgadinho",
            "brand": "Doritos",
            "size": "140g",
            "unit": "grama",
            "ean": "7891000600335",
            "image_url": "https://images.unsplash.com/photo-1613919113640-25732ec5e61f?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-034",
            "canonical_name": "chocolate barra lacta ao leite 90g",
            "display_name": "Chocolate Barra Lacta ao Leite 90g",
            "category": "doces",
            "subcategory": "chocolate",
            "brand": "Lacta",
            "size": "90g",
            "unit": "grama",
            "ean": "7891000600436",
            "image_url": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-035",
            "canonical_name": "bala fini tubes morango 80g",
            "display_name": "Bala Fini Tubes Morango 80g",
            "category": "doces",
            "subcategory": "bala",
            "brand": "Fini",
            "size": "80g",
            "unit": "grama",
            "ean": "7891000600537",
            "image_url": "https://images.unsplash.com/photo-1587985064048-c2a5292e8918?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-036",
            "canonical_name": "pipoca microondas popcorn manteiga 100g",
            "display_name": "Pipoca para Microondas Pop Corn Manteiga 100g",
            "category": "snacks",
            "subcategory": "pipoca",
            "brand": "Pop Corn",
            "size": "100g",
            "unit": "grama",
            "ean": "7891000600638",
            "image_url": "https://images.unsplash.com/photo-1578849278619-e73505e9610f?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Frutas e verduras (5 produtos)
        {
            "id": "prod-037",
            "canonical_name": "banana prata kg",
            "display_name": "Banana Prata (kg)",
            "category": "hortifruti",
            "subcategory": "frutas",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-038",
            "canonical_name": "tomate kg",
            "display_name": "Tomate (kg)",
            "category": "hortifruti",
            "subcategory": "legumes",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-039",
            "canonical_name": "batata inglesa kg",
            "display_name": "Batata Inglesa (kg)",
            "category": "hortifruti",
            "subcategory": "legumes",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-040",
            "canonical_name": "cebola kg",
            "display_name": "Cebola (kg)",
            "category": "hortifruti",
            "subcategory": "legumes",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1508313880080-c4bef43d4c1b?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-041",
            "canonical_name": "alface crespa unidade",
            "display_name": "Alface Crespa (unidade)",
            "category": "hortifruti",
            "subcategory": "verduras",
            "brand": "In Natura",
            "size": "1 unidade",
            "unit": "unidade",
            "image_url": "https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Carnes e proteínas (9 produtos)
        {
            "id": "prod-042",
            "canonical_name": "file peito frango kg",
            "display_name": "Filé de Peito de Frango (kg)",
            "category": "carnes",
            "subcategory": "aves",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-043",
            "canonical_name": "carne moida bovina kg",
            "display_name": "Carne Moída Bovina (kg)",
            "category": "carnes",
            "subcategory": "bovina",
            "brand": "In Natura",
            "size": "1000g",
            "unit": "kg",
            "image_url": "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-044",
            "canonical_name": "salsicha hot dog perdigao 500g",
            "display_name": "Salsicha Hot Dog Perdigão 500g",
            "category": "carnes",
            "subcategory": "embutidos",
            "brand": "Perdigão",
            "size": "500g",
            "unit": "grama",
            "ean": "7891000700144",
            "image_url": "https://images.unsplash.com/photo-1612743339061-8e4d46f8660e?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-045",
            "canonical_name": "presunto cozido sadia 200g",
            "display_name": "Presunto Cozido Sadia 200g",
            "category": "carnes",
            "subcategory": "embutidos",
            "brand": "Sadia",
            "size": "200g",
            "unit": "grama",
            "ean": "7891000700245",
            "image_url": "https://images.unsplash.com/photo-1562182384-08115de5ee97?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-046",
            "canonical_name": "ovo branco cartela 12 unidades",
            "display_name": "Ovo Branco Cartela 12 Unidades",
            "category": "carnes",
            "subcategory": "ovos",
            "brand": "In Natura",
            "size": "12 unidades",
            "unit": "unidade",
            "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        # Pães e padaria (5 produtos)
        {
            "id": "prod-047",
            "canonical_name": "pao forma integral wickbold 500g",
            "display_name": "Pão de Forma Integral Wickbold 500g",
            "category": "padaria",
            "subcategory": "pães",
            "brand": "Wickbold",
            "size": "500g",
            "unit": "grama",
            "ean": "7891000800147",
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-048",
            "canonical_name": "pao forma branco plus vita 500g",
            "display_name": "Pão de Forma Branco Plus Vita 500g",
            "category": "padaria",
            "subcategory": "pães",
            "brand": "Plus Vita",
            "size": "500g",
            "unit": "grama",
            "ean": "7891000800248",
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-049",
            "canonical_name": "bolo chocolate cacau show 300g",
            "display_name": "Bolo de Chocolate Cacau Show 300g",
            "category": "padaria",
            "subcategory": "bolos",
            "brand": "Cacau Show",
            "size": "300g",
            "unit": "grama",
            "ean": "7891000800349",
            "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "prod-050",
            "canonical_name": "torrada marilan integral 142g",
            "display_name": "Torrada Marilan Integral 142g",
            "category": "padaria",
            "subcategory": "torradas",
            "brand": "Marilan",
            "size": "142g",
            "unit": "grama",
            "ean": "7891000800450",
            "image_url": "https://images.unsplash.com/photo-1619785082615-0c4d5c7c7e1f?w=300",
            "created_at": datetime.now(timezone.utc).isoformat()
        },
    ]
    
    await db.products.delete_many({})
    await db.products.insert_many(products)
    print(f"✅ {len(products)} produto(s) adicionado(s)")
    return [p["id"] for p in products]


async def seed_offers(product_ids):
    """Cria ofertas variadas para os produtos em diferentes supermercados"""
    supermarket_ids = ["market-001", "market-002", "market-003", "market-004", "market-005"]
    
    # Preços base por produto (em R$)
    base_prices = {
        "prod-001": 5.99,  # Leite Itambé
        "prod-002": 5.50,
        "prod-003": 3.20,
        "prod-004": 8.90,
        "prod-005": 12.50,
        "prod-006": 22.90,  # Arroz 5kg
        "prod-007": 7.80,
        "prod-008": 7.50,
        "prod-009": 4.90,
        "prod-010": 4.20,
        "prod-011": 8.50,  # Coca 2L
        "prod-012": 7.90,
        "prod-013": 6.50,
        "prod-014": 2.20,
        "prod-015": 15.90,  # Café
        "prod-016": 3.80,
        "prod-017": 4.20,
        "prod-018": 7.90,
        "prod-019": 2.50,
        "prod-020": 3.20,
        "prod-021": 18.90,  # Papel higiênico
        "prod-022": 3.50,
        "prod-023": 16.90,
        "prod-024": 5.90,
        "prod-025": 12.50,
        "prod-026": 2.80,
        "prod-027": 3.90,
        "prod-028": 22.90,
        "prod-029": 5.50,
        "prod-030": 8.90,
        "prod-031": 4.20,
        "prod-032": 2.90,
        "prod-033": 7.50,
        "prod-034": 5.20,
        "prod-035": 4.50,
        "prod-036": 6.90,
        "prod-037": 4.50,  # Banana
        "prod-038": 5.90,  # Tomate
        "prod-039": 3.90,  # Batata
        "prod-040": 4.20,  # Cebola
        "prod-041": 2.50,  # Alface
        "prod-042": 18.90, # Frango
        "prod-043": 28.90, # Carne moída
        "prod-044": 8.90,
        "prod-045": 12.50,
        "prod-046": 14.90,  # Ovos
        "prod-047": 7.90,
        "prod-048": 6.50,
        "prod-049": 12.90,
        "prod-050": 5.50,
    }
    
    offers = []
    now = datetime.now(timezone.utc)
    
    # Criar 3-5 ofertas por produto (em supermercados diferentes)
    for product_id in product_ids:
        base_price = base_prices.get(product_id, 10.00)
        
        # Escolher 3-5 supermercados aleatórios
        selected_markets = random.sample(supermarket_ids, k=random.randint(3, 5))
        
        for market_id in selected_markets:
            # Variar preço por supermercado (-15% a +20%)
            variation = random.uniform(0.85, 1.20)
            price = round(base_price * variation, 2)
            
            # Algumas ofertas são promoções (20% de chance)
            is_promotion = random.random() < 0.20
            if is_promotion:
                price = round(price * 0.85, 2)  # 15% de desconto
            
            # Variar data de coleta (últimas 48 horas)
            hours_ago = random.randint(1, 48)
            collected_at = now - timedelta(hours=hours_ago)
            
            offer = {
                "id": f"offer-{product_id}-{market_id}",
                "product_id": product_id,
                "supermarket_id": market_id,
                "price": price,
                "unit_price": price,
                "currency": "BRL",
                "source": random.choice(["crowdsourced", "crowdsourced", "scraping"]),
                "confidence_score": random.uniform(0.85, 0.98),
                "collected_at": collected_at.isoformat(),
                "expires_at": (collected_at + timedelta(days=7)).isoformat(),
                "is_promotion": is_promotion,
                "stock_status": random.choice(["available", "available", "available", "low"]),
                "metadata": {
                    "user_id": "seed-user" if random.random() < 0.7 else None,
                    "photo_url": None,
                    "ocr_verified": False
                }
            }
            offers.append(offer)
    
    await db.offers.delete_many({})
    await db.offers.insert_many(offers)
    print(f"✅ {len(offers)} oferta(s) adicionada(s)")


async def main():
    print("🌱 Iniciando seed do banco de dados...\n")
    
    await seed_cities()
    await seed_supermarkets()
    product_ids = await seed_products()
    await seed_offers(product_ids)
    
    print("\n✨ Seed concluído com sucesso!")
    print("\n📊 Resumo:")
    print(f"   - 1 cidade (São Paulo)")
    print(f"   - 5 supermercados")
    print(f"   - 50 produtos")
    print(f"   - ~200 ofertas\n")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
