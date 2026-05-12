import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.models.seo_page import SEOPage
from app.services.seo_keywords import (
    SERVICE_LABELS, SERVICE_DESCRIPTIONS,
    COUNTIES_PRIORITY, INDUSTRIES,
    generate_keyword_matrix, prioritize_keywords,
)

logger = logging.getLogger(__name__)

PORTFOLIO_PLACEHOLDERS: dict[str, str] = {
    "logo-design": "https://placehold.co/600x400/1a1a1a/ffffff?text=Logo+Design",
    "brand-identity": "https://placehold.co/600x400/2d2d2d/ffffff?text=Brand+Identity",
    "advertising-marketing": "https://placehold.co/600x400/3d3d3d/ffffff?text=Advertising",
    "web-design-ui": "https://placehold.co/600x400/4d4d4d/ffffff?text=Web+Design+UI",
    "ux-design": "https://placehold.co/600x400/5d5d5d/ffffff?text=UX+Design",
    "publication-editorial": "https://placehold.co/600x400/6d6d6d/ffffff?text=Publication",
    "packaging-design": "https://placehold.co/600x400/7d7d7d/ffffff?text=Packaging",
    "environmental-experiential": "https://placehold.co/600x400/8d8d8d/ffffff?text=Experiential",
    "information-data-viz": "https://placehold.co/600x400/9d9d9d/ffffff?text=Data+Viz",
    "illustration-concept-art": "https://placehold.co/600x400/adadad/ffffff?text=Illustration",
    "environmental-graphics": "https://placehold.co/600x400/bdbdbd/ffffff?text=Environmental",
}


def generate_page_data(service: str, county: str, industry: str) -> dict:
    service_label = SERVICE_LABELS.get(service, service.replace("-", " ").title())
    service_desc = SERVICE_DESCRIPTIONS.get(service, f"Professional {service_label} services.")
    location = f"{county} County, Kenya"
    slug = f"{service}-in-{county.lower().replace(' ', '-')}-{industry.lower().replace(' ', '-')}"

    title = f"Best {service_label} Services in {county} | {industry} Design Expert"
    meta_description = (
        f"Looking for professional {service_label} in {county}? "
        f"Expert {industry.lower()} graphic designer offering {service_label} services in {location}. "
        f"Get a custom quote today."
    )
    h1 = f"{service_label} Services in {county} for {industry} Businesses"

    body_sections = [
        f"<h2>Professional {service_label} in {county}</h2>",
        f"<p>Are you a {industry.lower()} business in {county} looking for high-quality {service_label}? "
        f"As a Nairobi-based professional graphic designer serving all of Kenya, I specialize in creating "
        f"impactful visual designs tailored to {industry.lower()} companies in {location}.</p>",
        f"<h2>Why Choose a Professional {service_label} Designer?</h2>",
        f"<p>Your brand's visual identity speaks volumes about your {industry.lower()} business. "
        f"Professional {service_label} helps you stand out in {county}'s competitive market, "
        f"build trust with customers, and communicate your message effectively.</p>",
        f"<h2>What I Offer for {industry} Clients in {county}</h2>",
        f"<p>{service_desc} Every project includes unlimited revisions and source files, "
        f"ensuring you get exactly what your {industry.lower()} business needs.</p>",
        f"<h2>The Design Process</h2>",
        f"<p>1. Discovery: I learn about your {industry.lower()} business, goals, and preferences.<br>"
        f"2. Concept Development: I create initial design concepts for your review.<br>"
        f"3. Refinement: We collaborate on revisions until every detail is perfect.<br>"
        f"4. Delivery: You receive final print-ready and digital files.</p>",
        f"<h2>Why Businesses in {county} Trust Me</h2>",
        f"<p>With a track record of delivering outstanding {service_label} for clients across Kenya, "
        f"I understand the unique needs of {industry.lower()} businesses in {county}. "
        f"My commitment to quality, timely delivery, and client satisfaction sets me apart.</p>",
    ]
    body_html = "\n".join(body_sections)

    pricing_html = (
        f"<h3>Starting from KES 15,000</h3>"
        f"<p>Final pricing depends on project scope and complexity. "
        f"Contact me for a free, no-obligation quote tailored to your {industry.lower()} business.</p>"
    )

    cta_text = f"Get a Free Quote for {service_label} in {county}"

    schema_json = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{service_label} in {county}",
        "description": meta_description,
        "provider": {
            "@type": "Person",
            "name": "Graphic Designer",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": county,
                "addressRegion": "Kenya",
            },
        },
        "areaServed": {
            "@type": "City",
            "name": county,
        },
    }

    return {
        "slug": slug,
        "service_type": service,
        "county": county,
        "industry": industry,
        "title": title,
        "meta_description": meta_description,
        "h1": h1,
        "body_html": body_html,
        "portfolio_examples": [PORTFOLIO_PLACEHOLDERS.get(service, "")],
        "pricing_html": pricing_html,
        "cta_text": cta_text,
        "schema_json": schema_json,
    }


async def generate_and_publish_pages(batch_size: int = 50):
    matrix = generate_keyword_matrix()
    prioritized = prioritize_keywords(matrix)
    logger.info("SEO generator: %d total keyword combinations", len(prioritized))

    async with async_session_maker() as db:
        existing = await db.execute(select(SEOPage.slug))
        existing_slugs = {row[0] for row in existing.fetchall()}

        created = 0
        for item in prioritized:
            if created >= batch_size:
                break
            page_data = generate_page_data(item["service"], item["county"], item["industry"])
            if page_data["slug"] in existing_slugs:
                continue

            page = SEOPage(
                slug=page_data["slug"],
                service_type=page_data["service_type"],
                county=page_data["county"],
                industry=page_data["industry"],
                title=page_data["title"],
                meta_description=page_data["meta_description"],
                h1=page_data["h1"],
                body_html=page_data["body_html"],
                portfolio_examples=page_data["portfolio_examples"],
                pricing_html=page_data["pricing_html"],
                cta_text=page_data["cta_text"],
                schema_json=page_data["schema_json"],
                score=item["score"],
                published=True,
            )
            db.add(page)
            created += 1

        await db.commit()
        logger.info("SEO generator: created %d new pages", created)
        return {"total_combinations": len(prioritized), "created": created, "batch_size": batch_size}
