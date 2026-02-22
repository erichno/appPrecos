import unicodedata
import re
from typing import List


def normalize_text(text: str) -> str:
    """Normaliza texto para busca"""
    # Lowercase
    text = text.lower()
    
    # Remover acentos
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Remover stopwords
    stopwords = ["de", "da", "do", "para", "com", "sem", "o", "a"]
    words = text.split()
    words = [w for w in words if w not in stopwords]
    
    text = ' '.join(words)
    
    # Normalizar unidades
    text = re.sub(r'\b1\s?l\b', '1000ml', text)
    text = re.sub(r'\b2\s?l\b', '2000ml', text)
    text = re.sub(r'\b(\d+)\s?kg\b', lambda m: f"{int(m.group(1))*1000}g", text)
    text = re.sub(r'\b(\d+)\s?litros?\b', lambda m: f"{int(m.group(1))*1000}ml", text)
    
    # Sinônimos comuns
    text = text.replace("refri", "refrigerante")
    text = text.replace("coca", "coca-cola")
    
    return text.strip()


def calculate_similarity(str1: str, str2: str) -> float:
    """Calcula similaridade entre duas strings (0-1)"""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str1, str2).ratio()
