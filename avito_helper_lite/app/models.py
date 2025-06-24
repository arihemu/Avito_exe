"""Database models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ItemStat(Base):
    __tablename__ = "item_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[str]
    date: Mapped[datetime]
    views: Mapped[int]


class CompetitorItem(Base):
    __tablename__ = "competitor_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[str]
    seller_id: Mapped[str]
    price: Mapped[int]
    last_seen: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    views: Mapped[int] | None

    history: Mapped[list[CompetitorView]] = relationship(
        "CompetitorView", back_populates="item", cascade="all, delete-orphan"
    )


class CompetitorView(Base):
    __tablename__ = "competitor_views"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("competitor_items.id"))
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    views: Mapped[int]

    item: Mapped[CompetitorItem] = relationship(
        "CompetitorItem", back_populates="history"
    )
