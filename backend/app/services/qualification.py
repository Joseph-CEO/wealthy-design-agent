import logging
from typing import Optional
from app.models.lead import Lead

logger = logging.getLogger(__name__)

# Services this designer offers
OFFERED_SERVICES = [
    # Brand / Identity Design
    "logo design", "logo", "branding", "brand identity", "visual identity",
    "brand guidelines", "stationery design", "social media branding",
    # Advertising / Marketing Design
    "advertising", "marketing design", "print ad", "outdoor ad",
    "digital ad", "social media campaign", "email marketing",
    "event marketing", "motion ad", "video ad", "pos display",
    # Web Design / UI
    "website design", "website", "web design", "ui design",
    "app interface", "landing page", "web ui",
    # UX Design
    "ux design", "user experience", "wireframe", "interactive prototype",
    "user journey", "usability", "information architecture",
    # Publication / Editorial Design
    "book layout", "book cover", "book design", "editorial design",
    "magazine layout", "publication design", "annual report",
    "catalogue", "newsletter", "digital publication",
    "ngo publication", "educational material",
    # Packaging Design
    "packaging design", "packaging", "product label",
    "structural dieline", "unboxing",
    # Environmental / Experiential Design
    "signboard", "signage", "wayfinding", "exhibition graphics",
    "office branding", "retail graphics", "event backdrop",
    # Information / Data Visualization
    "infographic", "data visualization", "dashboard design",
    "data report", "educational diagram",
    # Illustration / Concept Art
    "illustration", "concept art", "vector art", "poster art",
    "custom graphic", "editorial illustration",
    # Environmental Graphics
    "wall mural", "large format branding", "public installation",
    "architectural branding",
    # Legacy granular types
    "flyer", "flyers", "poster", "posters",
    "menu design", "menu", "banner", "banners",
]

SERVICE_KEYWORDS = set(OFFERED_SERVICES)


def score_lead(lead: Lead) -> int:
    """
    Score a lead 0-100 based on relevance to offered services.
    Uses keyword matching + title/description analysis.
    Phase 3 will upgrade this to GPT-4o NLP scoring.
    """
    score = 0
    text = f"{lead.title or ''} {lead.description or ''}".lower()

    # Service relevance (up to 60 points)
    matched_services = 0
    for kw in SERVICE_KEYWORDS:
        if kw in text:
            matched_services += 1
    score += min(matched_services * 15, 60)

    # Budget indicator (up to 20 points)
    if lead.budget_max and lead.budget_max > 50:
        score += 10
        if lead.budget_max > 200:
            score += 5
        if lead.budget_max > 500:
            score += 5

    # Has client contact info (up to 10 points)
    if lead.client_email:
        score += 10
    elif lead.client_name:
        score += 5

    # Description quality (up to 10 points)
    if lead.description:
        desc_len = len(lead.description)
        if desc_len > 200:
            score += 10
        elif desc_len > 100:
            score += 5

    return min(score, 100)


async def qualify_lead(lead: Lead, threshold: int = 70) -> tuple[int, str]:
    """
    Determine if a lead should be pursued.
    Returns (score, decision) where decision is:
      - "qualified" if score >= threshold
      - "low_priority" if score < threshold
    """
    score = score_lead(lead)
    decision = "qualified" if score >= threshold else "low_priority"
    logger.info(
        "Lead %d scored %d/100 → %s",
        lead.id, score, decision,
    )
    return score, decision
