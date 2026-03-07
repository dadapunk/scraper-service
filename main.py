from fastapi import FastAPI, HTTPException
from datetime import datetime, UTC
from models import SearchRequest, SearchResponse, ErrorResponse
from scrapers import SCRAPERS
import logging

app = FastAPI(title="Scraper Service", version="0.1.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(UTC).isoformat()}

@app.post("/search", response_model=SearchResponse, responses={400: {"model": ErrorResponse}})
async def search(request: SearchRequest):
    source = request.source.lower()
    query = request.query
    limit = request.limit
    
    if source not in SCRAPERS:
        raise HTTPException(status_code=400, detail=f"Unknown source: {source}")
    
    try:
        scraper = SCRAPERS[source]
        results = await scraper.search(query, limit)
        
        return SearchResponse(
            source=source,
            query=query,
            results=results,
            scraped_at=datetime.now(UTC)
        )
    
    except Exception as e:
        logger.error(f"Error scraping {source} for query '{query}': {e}")
        return ErrorResponse(
            source=source,
            query=query,
            error=str(e),
            scraped_at=datetime.now(UTC)
        )
