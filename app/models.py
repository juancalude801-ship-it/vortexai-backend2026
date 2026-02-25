from sqlalchemy import String, Integer, DateTime, Float, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db import Base

class Buyer(Base):
    __tablename__ = "buyers"
    __table_args__ = (UniqueConstraint("email", "city", "state", name="uq_buyer_email_city_state"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), index=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(20), index=True)
    min_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    strategy: Mapped[str | None] = mapped_column(String(40), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SellerLead(Base):
    __tablename__ = "seller_leads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    full_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[str | None] = mapped_column(String(180), nullable=True)

    property_address: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(20), index=True)

    reason: Mapped[str | None] = mapped_column(String(80), nullable=True)
    asking_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timeline: Mapped[str | None] = mapped_column(String(60), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(40), default="rentcast")
    external_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    address: Mapped[str] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(20), index=True)
    zipcode: Mapped[str | None] = mapped_column(String(20), nullable=True)

    list_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    beds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    baths: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    property_type: Mapped[str | None] = mapped_column(String(60), nullable=True)

    arv: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repairs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mao: Mapped[int | None] = mapped_column(Integer, nullable=True)

    score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="new")  # new/green/orange/red/blasted/under_contract

    last_blasted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ContractFile(Base):
    __tablename__ = "contract_files"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(Integer, index=True)
    filename: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
