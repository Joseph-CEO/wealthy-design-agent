import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, DateTime, JSON
from app.database import Base


class PortfolioCategory(str, enum.Enum):
    branding = "branding"
    logo_design = "logo_design"
    advertising_marketing = "advertising_marketing"
    web_ui = "web_ui"
    website = "website"
    ux_design = "ux_design"
    publication_editorial = "publication_editorial"
    book_layout = "book_layout"
    book_cover = "book_cover"
    packaging_design = "packaging_design"
    environmental_experiential = "environmental_experiential"
    signboard = "signboard"
    information_data_viz = "information_data_viz"
    illustration_concept_art = "illustration_concept_art"
    environmental_graphics = "environmental_graphics"
    flyer = "flyer"
    poster = "poster"
    menu = "menu"
    banner = "banner"


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(PortfolioCategory), nullable=False, index=True)
    image_urls = Column(JSON, default=list)
    project_url = Column(String(500), nullable=True)
    tags = Column(JSON, default=list)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
