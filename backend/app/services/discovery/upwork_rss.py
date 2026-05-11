import logging
from typing import Optional
from httpx import AsyncClient

logger = logging.getLogger(__name__)

UPWORK_RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss"

GRAPHIC_DESIGN_QUERIES = [
    "graphic+design",
    "logo+design",
    "branding",
    "book+layout",
    "book+cover",
    "packaging+design",
    "signboard",
    "flyer+design",
    "poster+design",
    "menu+design",
    "banner+design",
    "website+design",
]


class UpworkRSSFeed:
    def __init__(self):
        self.client = AsyncClient(timeout=30.0)

    async def fetch(self, query: str) -> list[dict]:
        url = f"{UPWORK_RSS_URL}?q={query}&sort=recency"
        try:
            resp = await self.client.get(url)
            resp.raise_for_status()
            return self._parse_xml(resp.text)
        except Exception as e:
            logger.warning("Upwork RSS fetch failed for '%s': %s", query, e)
            return []

    async def fetch_all(self, max_results: int = 50) -> list[dict]:
        logger.info("Fetching Upwork RSS feeds...")
        all_items: list[dict] = []
        for query in GRAPHIC_DESIGN_QUERIES:
            items = await self.fetch(query)
            all_items.extend(items)
            if len(all_items) >= max_results:
                break
        return all_items[:max_results]

    def _parse_xml(self, raw: str) -> list[dict]:
        items: list[dict] = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(raw)
            ns = {"rss": "http://purl.org/rss/1.0/", "dc": "http://purl.org/dc/elements/1.1/"}
            for item_elem in root.iter("item") if root.tag == "rss" else root.findall(".//item"):
                title_el = item_elem.find("title")
                link_el = item_elem.find("link")
                desc_el = item_elem.find("description")
                title = title_el.text if title_el is not None else ""
                link = link_el.text if link_el is not None else ""
                desc = desc_el.text if desc_el is not None else ""
                items.append({
                    "title": title,
                    "url": link,
                    "description": desc[:2000] if desc else "",
                })
        except ET.ParseError as e:
            logger.error("Failed to parse Upwork RSS XML: %s", e)
        logger.info("Parsed %d items from Upwork RSS", len(items))
        return items

    async def close(self):
        await self.client.aclose()

    @staticmethod
    def normalize(item: dict) -> dict:
        return {
            "external_id": item.get("url", ""),
            "title": item.get("title", "Untitled Upwork Job"),
            "description": item.get("description", ""),
            "client_name": None,
            "budget_min": None,
            "budget_max": None,
            "currency": "USD",
            "location": None,
            "source": "upwork",
        }
