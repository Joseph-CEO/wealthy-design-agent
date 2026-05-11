import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.services.discovery.apify_client import ApifyClient
from app.services.discovery.upwork_rss import UpworkRSSFeed
from app.models.lead import Lead, LeadStatus

logger = logging.getLogger(__name__)


class DiscoveryOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_full_scan(self) -> dict:
        """Run all discovery sources and return summary."""
        summary: dict[str, int] = {"dribbble": 0, "freelancer": 0, "upwork": 0, "total_new": 0}

        if settings.apify_api_key:
            apify = ApifyClient(settings.apify_api_key)
            try:
                dribbble_items = await apify.scrape_dribbble()
                saved = await self._save_leads(dribbble_items, apify.normalize_dribbble, "dribbble")
                summary["dribbble"] = saved

                freelancer_items = await apify.scrape_freelancer()
                saved = await self._save_leads(freelancer_items, apify.normalize_freelancer, "freelancer")
                summary["freelancer"] = saved
            finally:
                await apify.close()

        upwork = UpworkRSSFeed()
        try:
            upwork_items = await upwork.fetch_all()
            saved = await self._save_leads(upwork_items, upwork.normalize, "upwork")
            summary["upwork"] = saved
        finally:
            await upwork.close()

        summary["total_new"] = summary["dribbble"] + summary["freelancer"] + summary["upwork"]
        logger.info("Discovery scan complete: %s", summary)
        return summary

    async def _save_leads(
        self,
        raw_items: list[dict],
        normalizer,
        source: str,
    ) -> int:
        if not raw_items:
            return 0

        from sqlalchemy import select

        new_count = 0
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            normalized = normalizer(item)
            external_id = normalized.get("external_id", "")
            if external_id:
                existing = await self.db.execute(
                    select(Lead).where(
                        Lead.external_id == external_id,
                        Lead.source == source,
                    )
                )
                if existing.scalar_one_or_none():
                    continue

            lead = Lead(
                source=source,
                external_id=external_id,
                title=normalized.get("title", "")[:500],
                description=normalized.get("description", ""),
                client_name=normalized.get("client_name"),
                budget_min=normalized.get("budget_min"),
                budget_max=normalized.get("budget_max"),
                currency=normalized.get("currency", "USD"),
                location=normalized.get("location"),
                status=LeadStatus.new,
                raw_data=item,
            )
            self.db.add(lead)
            new_count += 1

        if new_count:
            await self.db.commit()
            logger.info("Saved %d new leads from %s", new_count, source)

        return new_count
