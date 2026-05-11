import logging
from typing import Optional
from httpx import AsyncClient, HTTPError

logger = logging.getLogger(__name__)

APIFY_BASE = "https://api.apify.com/v2"

# Apify Actor IDs for job scraping
DRIBBBLE_ACTOR_ID = "shahidirfan~dribbble-jobs-scraper"
FREELANCER_ACTOR_ID = "scrapestorm~freelancer-com-jobs-scraper---cheap"

GRAPHIC_DESIGN_KEYWORDS = [
    "graphic design",
    "logo design",
    "branding",
    "book layout",
    "book cover",
    "packaging design",
    "signboard",
    "flyer design",
    "poster design",
    "menu design",
    "banner design",
    "website design",
    "visual identity",
]


class ApifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncClient(timeout=60.0)

    async def _run_actor(
        self, actor_id: str, input_data: dict, max_items: int = 50
    ) -> list[dict]:
        url = f"{APIFY_BASE}/acts/{actor_id}/run-sync-get-dataset-items"
        params = {"token": self.api_key}
        input_data.setdefault("proxyConfiguration", {
            "useApifyProxy": True,
        })
        try:
            resp = await self.client.post(url, params=params, json=input_data)
            resp.raise_for_status()
            items = resp.json()
            logger.info("Apify actor %s returned %d items", actor_id, len(items))
            return items[:max_items] if isinstance(items, list) else []
        except HTTPError as e:
            logger.error("Apify actor %s failed: %s", actor_id, e)
            return []

    async def scrape_dribbble(self, max_results: int = 50) -> list[dict]:
        logger.info("Scraping Dribbble for design jobs...")
        input_data = {
            "specialties": [
                "brand-graphic-design",
                "ui-visual-design",
                "illustration",
                "web-design",
                "product-design",
            ],
            "freelanceOrContract": True,
            "openToRemote": True,
            "maxResults": max_results,
        }
        return await self._run_actor(DRIBBBLE_ACTOR_ID, input_data)

    async def scrape_freelancer(self, max_items: int = 50) -> list[dict]:
        logger.info("Scraping Freelancer.com for design projects...")
        all_results: list[dict] = []
        for keyword in GRAPHIC_DESIGN_KEYWORDS:
            input_data = {
                "keyword": keyword,
                "language": "english",
                "job_state": "open",
                "max_items": max(1, max_items // len(GRAPHIC_DESIGN_KEYWORDS)),
            }
            results = await self._run_actor(FREELANCER_ACTOR_ID, input_data)
            all_results.extend(results)
        return all_results[:max_items]

    async def close(self):
        await self.client.aclose()

    @staticmethod
    def normalize_dribbble(item: dict) -> dict:
        return {
            "external_id": item.get("url", ""),
            "title": item.get("title", "Untitled Dribbble Job"),
            "description": item.get("description", ""),
            "client_name": item.get("company", {}).get("name") if isinstance(item.get("company"), dict) else None,
            "budget_min": None,
            "budget_max": None,
            "currency": "USD",
            "location": item.get("location"),
            "source": "dribbble",
        }

    @staticmethod
    def normalize_freelancer(item: dict) -> dict:
        return {
            "external_id": item.get("url", ""),
            "title": item.get("title", "Untitled Freelancer Project"),
            "description": item.get("description", ""),
            "client_name": item.get("employer", {}).get("username") if isinstance(item.get("employer"), dict) else None,
            "budget_min": item.get("budget", {}).get("minimum"),
            "budget_max": item.get("budget", {}).get("maximum"),
            "currency": item.get("currency", {}).get("code", "USD") if isinstance(item.get("currency"), dict) else "USD",
            "location": None,
            "source": "freelancer",
        }
