from scrapers.supermarkets.bonpreu import BonpreuScraper
from scrapers.supermarkets.lidl import LidlScraper

SCRAPERS = {
    "bonpreu": BonpreuScraper(),
    "lidl": LidlScraper(),
}
