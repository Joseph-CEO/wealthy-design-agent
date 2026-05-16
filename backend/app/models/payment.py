import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, Enum, DateTime, ForeignKey
from app.database import Base


class PaymentGateway(str, enum.Enum):
    pesapal = "pesapal"
    mpesa = "mpesa"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    gateway = Column(Enum(PaymentGateway), nullable=False)
    gateway_payment_id = Column(String(255), nullable=True)
    gateway_status = Column(String(50), nullable=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, index=True)
    client_email = Column(String(255), nullable=True)
    receipt_url = Column(String(500), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
