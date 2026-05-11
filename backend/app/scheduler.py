import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.database import async_session_maker
from app.services.discovery.orchestrator import DiscoveryOrchestrator
from app.services.seo_generator import generate_and_publish_pages
from app.models.scan_log import ScanLog

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def discovery_scan_job():
    logger.info("Discovery scan triggered — scanning for new leads...")
    async with async_session_maker() as db:
        scan_log = ScanLog(
            scan_type="full_discovery",
            status="running",
            started_at=datetime.now(timezone.utc),
        )
        db.add(scan_log)
        await db.commit()
        await db.refresh(scan_log)

        orchestrator = DiscoveryOrchestrator(db)
        try:
            summary = await orchestrator.run_full_scan()
            total_found = summary.get("total_new", 0)
            scan_log.status = "completed"
            scan_log.leads_found = total_found
            scan_log.message = f"Dribbble={summary.get('dribbble', 0)}, Freelancer={summary.get('freelancer', 0)}, Upwork={summary.get('upwork', 0)}"
            scan_log.completed_at = datetime.now(timezone.utc)
            logger.info("Discovery scan complete: %s", summary)
        except Exception as e:
            scan_log.status = "failed"
            scan_log.message = str(e)
            scan_log.completed_at = datetime.now(timezone.utc)
            logger.error("Discovery scan failed: %s", e, exc_info=True)
        finally:
            await db.commit()


async def seo_generation_job():
    logger.info("SEO generation triggered — generating new SEO pages...")
    try:
        result = await generate_and_publish_pages(batch_size=settings.seo_batch_size)
        logger.info("SEO generation complete: %s", result)
    except Exception as e:
        logger.error("SEO generation failed: %s", e, exc_info=True)


def start_scheduler():
    interval_hours = max(settings.scan_interval_hours, 1)
    scheduler.add_job(
        discovery_scan_job,
        "interval",
        hours=interval_hours,
        id="discovery_scan",
        replace_existing=True,
    )
    seo_interval_hours = max(settings.seo_interval_hours, 168)
    scheduler.add_job(
        seo_generation_job,
        "interval",
        hours=seo_interval_hours,
        id="seo_generation",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started — scanning every %d hour(s), SEO every %d hour(s).",
                interval_hours, seo_interval_hours)


def stop_scheduler():
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped.")
