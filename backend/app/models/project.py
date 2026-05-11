import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Enum, DateTime, ForeignKey
from app.database import Base


class ProjectStatus(str, enum.Enum):
    brief = "brief"
    negotiation = "negotiation"
    in_progress = "in_progress"
    review = "review"
    delivered = "delivered"
    paid = "paid"
    cancelled = "cancelled"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.brief, index=True)
    quote_amount = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    client_email = Column(String(255), nullable=True)
    started_at = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
