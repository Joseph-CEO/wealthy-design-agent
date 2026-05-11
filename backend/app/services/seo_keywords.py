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
    return min(score, 100)

def prioritize_keywords(matrix: list[dict]) -> list[dict]:
    for item in matrix:
        item["score"] = score_opportunity(item["service"], item["county"], item["industry"])
    matrix.sort(key=lambda x: x["score"], reverse=True)
    return matrix
