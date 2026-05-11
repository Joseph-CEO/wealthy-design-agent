from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from app.database import Base


class SEOPage(Base):
    __tablename__ = "seo_pages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    service_type = Column(String(100), nullable=False, index=True)
    county = Column(String(100), nullable=False, index=True)
    industry = Column(String(100), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    meta_description = Column(String(500), nullable=False)
    h1 = Column(String(500), nullable=False)
    body_html = Column(Text, nullable=True)
    portfolio_examples = Column(JSON, default=list)
    pricing_html = Column(Text, nullable=True)
    cta_text = Column(String(500), nullable=True)
    schema_json = Column(JSON, nullable=True)
    score = Column(Integer, default=0)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
