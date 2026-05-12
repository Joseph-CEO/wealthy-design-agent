import logging

from app.services.google_ads import google_ads

logger = logging.getLogger(__name__)

SERVICES = [
    "logo-design", "brand-identity", "advertising-marketing",
    "web-design-ui", "ux-design", "publication-editorial",
    "packaging-design", "environmental-experiential",
    "information-data-viz", "illustration-concept-art",
    "environmental-graphics",
]

SERVICE_LABELS = {
    "logo-design": "Logo Design",
    "brand-identity": "Brand Identity",
    "advertising-marketing": "Advertising & Marketing Design",
    "web-design-ui": "Web Design & UI",
    "ux-design": "UX Design",
    "publication-editorial": "Publication & Editorial Design",
    "packaging-design": "Packaging Design",
    "environmental-experiential": "Environmental & Experiential Design",
    "information-data-viz": "Information & Data Visualization",
    "illustration-concept-art": "Illustration & Concept Art",
    "environmental-graphics": "Environmental Graphics",
}

SERVICE_DESCRIPTIONS = {
    "logo-design": "Custom logo design that captures your brand essence with multiple concepts, color variations, and vector files.",
    "brand-identity": "Complete visual identity systems including logo, color palette, typography, brand guidelines, and application mockups.",
    "advertising-marketing": "Promotional design across channels — print ads, outdoor ads, digital ads, social media campaigns, email marketing, and motion ads.",
    "web-design-ui": "Visual design of websites and digital interfaces — layouts, app screens, and responsive designs.",
    "ux-design": "User experience design focusing on usability, flow, wireframes, interactive prototypes, user journey maps, and personas.",
    "publication-editorial": "Layout and design for long-form print and digital publications — magazines, books, annual reports, catalogues, and newsletters.",
    "packaging-design": "Product packaging design including labels, structural dielines, boxes, and branded unboxing experiences.",
    "environmental-experiential": "Graphics integrated into physical spaces — signage, wayfinding, exhibition graphics, office branding, retail graphics, and event stage backdrops.",
    "information-data-viz": "Clear visual communication of complex data — infographics, dashboards, data reports, and educational diagrams.",
    "illustration-concept-art": "Custom artwork for storytelling, branding, or visualization — editorial illustrations, vector art, poster art.",
    "environmental-graphics": "Large-scale graphics for public or branded spaces — wall murals, large-format branding, public installations, and branded architectural elements.",
}

COUNTIES_PRIORITY = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
    "Meru", "Machakos", "Kiambu", "Kisii", "Malindi",
    "Kitale", "Nyeri", "Kakamega", "Thika", "Naivasha",
    "Garissa", "Nanyuki", "Voi", "Lamu", "Isiolo",
    "Embu", "Busia", "Bungoma", "Homa Bay", "Migori",
    "Siaya", "Kericho", "Nandi", "Uasin Gishu", "Trans Nzoia",
    "Laikipia", "Muranga", "Kirinyaga", "Nyandarua", "Makueni",
    "Kitui", "Taita Taveta", "Tana River", "Kilifi", "Kwale",
    "Mandera", "Wajir", "Marsabit", "Turkana", "West Pokot",
    "Samburu", "Elgeyo Marakwet",
]

INDUSTRIES = [
    "Technology", "Hospitality", "Healthcare", "Education", "Agriculture",
    "Real Estate", "Retail", "Finance", "Manufacturing", "Transport",
    "Entertainment", "Non-Profit", "Fashion", "Food & Beverage",
    "Construction", "Energy", "Tourism", "Sports", "Media",
]

_volume_cache: dict[str, dict] | None = None


def _build_query_phrases() -> list[str]:
    phrases = []
    for service in SERVICES[:5]:
        label = SERVICE_LABELS[service]
        for county in COUNTIES_PRIORITY[:5]:
            phrases.append(f"{label} {county} Kenya")
    return phrases


def refresh_search_volume_cache():
    global _volume_cache
    phrases = _build_query_phrases()
    logger.info("Google Ads: fetching search volume for %d phrases", len(phrases))
    data = google_ads.get_keyword_ideas(phrases)
    if data:
        _volume_cache = data
        logger.info("Google Ads: cached %d keyword volume results", len(data))
    else:
        _volume_cache = {}


def get_volume_for(service: str, county: str) -> int:
    if _volume_cache is None:
        return -1
    label = SERVICE_LABELS.get(service, "")
    phrase = f"{label} {county} Kenya"
    entry = _volume_cache.get(phrase)
    if entry:
        return entry.get("avg_monthly_searches", 0)
    return -1


def generate_keyword_matrix():
    matrix = []
    for service in SERVICES:
        for county in COUNTIES_PRIORITY:
            for industry in INDUSTRIES:
                matrix.append({
                    "service": service,
                    "county": county,
                    "industry": industry,
                })
    return matrix

def score_opportunity(service: str, county: str, _industry: str) -> int:
    score = 50
    county_rank = COUNTIES_PRIORITY.index(county) if county in COUNTIES_PRIORITY else len(COUNTIES_PRIORITY)
    score += max(0, 50 - county_rank)

    volume = get_volume_for(service, county)
    if volume >= 100:
        score += 25
    elif volume >= 50:
        score += 15
    elif volume >= 10:
        score += 5
    elif volume == 0:
        score -= 10

    return max(0, min(score, 100))

def prioritize_keywords(matrix: list[dict]) -> list[dict]:
    refresh_search_volume_cache()
    for item in matrix:
        item["score"] = score_opportunity(item["service"], item["county"], item["industry"])
    matrix.sort(key=lambda x: x["score"], reverse=True)
    return matrix
