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


class RealEstateResult(SearchResult):
    price: float
    price_per_m2: Optional[float] = None
    size: Optional[float] = None  # meters squared
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    location: Optional[str] = None
    property_type: Optional[str] = None  # house, apartment, etc.
    operation_type: Optional[str] = None  # rent, sale


class SearchResponse(BaseModel):
    source: str
    query: str
    results: List[SearchResult]  # Changed to base class to support multiple types
    error: Optional[str] = None
    scraped_at: datetime


class ErrorResponse(BaseModel):
    source: str
    query: str
    results: List[SearchResult] = []  # Changed to base class
    error: str
    scraped_at: datetime
