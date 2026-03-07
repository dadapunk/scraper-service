"""Manual smoke test — run with: python tests/smoke_test.py (service must be running on :8090)"""
import httpx
import asyncio

async def run():
    async with httpx.AsyncClient() as client:
        health_response = await client.get("http://localhost:8090/health")
        print("Health:", health_response.status_code, health_response.json())

        search_response = await client.post("http://localhost:8090/search", json={
            "source": "bonpreu",
            "query": "queso manchego",
            "limit": 3,
        })
        print("Search:", search_response.status_code, search_response.json())

if __name__ == "__main__":
    asyncio.run(run())
