from abc import ABC, abstractmethod
from typing import List
from models import SupermarketResult

class Scraper(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[SupermarketResult]:
        pass
