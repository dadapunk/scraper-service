import json
import httpx
from typing import List
from config import get_settings
from models import SupermarketResult

SYSTEM_PROMPT = """
Eres un asistente que extrae productos de supermercado de páginas web en formato Markdown.
Dado el contenido Markdown de una página de búsqueda de supermercado y el término buscado, extrae los productos encontrados.

Devuelve un JSON con:
{"products": [
  {"name": "nombre completo del producto", "brand": "marca", "price": 2.49, "unit": "ud", "unit_price": 16.6},
  ...
]}

- price: precio en euros (número)
- unit: unidad de venta apropiada para el producto:
  - "ud" para productos vendidos por unidad (botellas, latas, paquetes, piezas)
  - "kg" para productos vendidos por kilo
  - "g" para productos vendidos por gramos
  - "l" para productos vendidos por litro
  - "ml" para productos vendidos por mililitros
- unit_price: precio por kg o litro si aparece en la página, 0 si no
- IMPORTANTE: incluye ÚNICAMENTE productos que sean exactamente del mismo tipo de alimento o bebida que el término buscado.
  Si buscas "zumo" incluye solo zumos. Si buscas "cerveza" incluye solo cervezas. Si buscas "jamón" incluye solo jamones.
  NO incluyas productos de otras categorías aunque aparezcan en la misma página.
- Si no hay productos del mismo tipo, devuelve {"products": []}
""".strip()

def _is_quota_error(message: str) -> bool:
    return any(k in message for k in ("429", "RESOURCE_EXHAUSTED", "quota"))

async def extract_products_from_markdown(markdown: str, query: str) -> List[SupermarketResult]:
    settings = get_settings()
    models = settings.llm_models
    if not models:
        raise ValueError("No LLM models configured")

    last_err: Exception | None = None
    for i, model in enumerate(models):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{settings.llm_base_url}/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.llm_api_key}",
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Termino buscado: {query}\n\nContenido de la página:\n{markdown}"},
                        ],
                        "temperature": 0.0,
                        "response_format": {"type": "json_object"},
                    },
                )

                if _is_quota_error(str(response.status_code) + response.text):
                    last_err = Exception(f"Quota exceeded for model {model}")
                    if i < len(models) - 1:
                        import logging
                        logging.warning("LLM quota exceeded, trying fallback model: %s -> %s", model, models[i + 1])
                        continue
                    raise last_err

                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                result = json.loads(content)

                return [
                    SupermarketResult(
                        title=p["name"],
                        price=p["price"],
                        unit=p.get("unit"),
                        unit_price=p.get("unit_price"),
                        brand=p.get("brand"),
                        url="",
                    )
                    for p in result.get("products", [])
                ]

        except Exception as e:
            if _is_quota_error(str(e)) and i < len(models) - 1:
                last_err = e
                continue
            raise

    raise last_err or Exception("All LLM models failed")
