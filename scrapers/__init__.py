from scrapers.supermarkets.bonpreu import BonpreuScraper
from scrapers.supermarkets.lidl import LidlScraper
from scrapers.realestate.idealista import IdealistaScraper

SCRAPERS = {
    "bonpreu": BonpreuScraper(),
    "lidl": LidlScraper(),
    "idealista": IdealistaScraper(),
}
