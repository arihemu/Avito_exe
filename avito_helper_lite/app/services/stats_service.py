"""Service for collecting daily views."""

from __future__ import annotations

import datetime as dt
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..core.avito_client import AvitoClient
from ..models import Base, ItemStat


class StatsService:
    def __init__(self, client: AvitoClient, account_id: str, db_url: str) -> None:
        self.client = client
        self.account_id = account_id
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def collect_daily_views(self) -> None:
        items = self.client.get_items_stats(self.account_id)
        with Session(self.engine) as session:
            for item in items:
                stat = ItemStat(
                    item_id=str(item["item_id"]),
                    date=dt.datetime.utcnow().date(),
                    views=item["counters"]["views_total"],
                )
                session.add(stat)
            session.commit()
