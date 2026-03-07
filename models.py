from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    source: str
    query: str
    limit: int = 10

class SearchResult(BaseModel):
    title: str
    url: str
    image_url: Optional[str] = None
    metadata: dict = {}

class SupermarketResult(SearchResult):
    price: float
    unit: Optional[str] = None
    amount: Optional[float] = None
    unit_price: Optional[float] = None
    brand: Optional[str] = None

class SearchResponse(BaseModel):
    source: str
    query: str
    results: List[SupermarketResult]
    error: Optional[str] = None
    scraped_at: datetime

class ErrorResponse(BaseModel):
    source: str
    query: str
    results: List[SupermarketResult] = []
    error: str
    scraped_at: datetime
