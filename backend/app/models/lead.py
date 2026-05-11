import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Enum, DateTime, JSON
from app.database import Base


class ServiceType(str, enum.Enum):
    # Brand / Identity Design
    branding = "branding"
    logo_design = "logo_design"
    # Advertising / Marketing Design
    advertising_marketing = "advertising_marketing"
    # Web Design / UI
    web_ui = "web_ui"
    website = "website"
    # UX Design
    ux_design = "ux_design"
    # Publication / Editorial Design
    publication_editorial = "publication_editorial"
    book_layout = "book_layout"
    book_cover = "book_cover"
    # Packaging Design
    packaging_design = "packaging_design"
    # Environmental / Experiential Design
    environmental_experiential = "environmental_experiential"
    signboard = "signboard"
    # Information / Data Visualization
    information_data_viz = "information_data_viz"
    # Illustration / Concept Art
    illustration_concept_art = "illustration_concept_art"
    # Environmental Graphics
    environmental_graphics = "environmental_graphics"
    # Legacy granular types
    flyer = "flyer"
    poster = "poster"
    menu = "menu"
    banner = "banner"
    other = "other"


class LeadStatus(str, enum.Enum):
    new = "new"
    qualified = "qualified"
    contacted = "contacted"
    engaged = "engaged"
    negotiating = "negotiating"
    converted = "converted"
    closed = "closed"
    low_priority = "low_priority"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False, index=True)
    external_id = Column(String(255), nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    client_name = Column(String(255), nullable=True)
    client_email = Column(String(255), nullable=True)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    location = Column(String(255), nullable=True)
    service_type = Column(Enum(ServiceType), nullable=True)
    score = Column(Integer, default=0)
    status = Column(Enum(LeadStatus), default=LeadStatus.new, index=True)
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
