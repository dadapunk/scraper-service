FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

# Install uv
RUN pip install uv --no-cache-dir

# Copy dependency manifest first (layer cache)
COPY pyproject.toml .

# Install production deps only, using system Python from base image
RUN uv sync --no-dev

# Copy application code
COPY main.py config.py models.py llm.py ./
COPY scrapers/ scrapers/

EXPOSE 8090

CMD ["uv", "run", "--no-dev", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
