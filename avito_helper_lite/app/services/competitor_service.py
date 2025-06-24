"""Service to track competitor items."""

from __future__ import annotations

import datetime as dt

from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from ..models import Base, CompetitorItem, CompetitorView

SEARCH_URL = (
    "https://www.avito.ru/voronezhskaya_oblast/mebel_i_interer/kuhonnye_garnitury/"
    "kukhni-ASgBAgICAkRazk_W6hKMso0D?cd=1&f=ASgBAgECAkRazk_W6hKMso0DAUXGmgwVeyJmcm9tIjo1MDAwMCwidG8iOjB9&q=кухни+на+заказ"
)


class CompetitorService:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def track(self) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(SEARCH_URL)
            page.wait_for_load_state("networkidle")

            items = page.query_selector_all("div[data-marker='item']")[:20]
            data = []
            for it in items:
                item_id = it.get_attribute("data-item-id")
                seller_id = it.get_attribute("data-owner-id") or ""
                price_text = it.query_selector(
                    "span[data-marker='item-price']"
                ).inner_text()
                price = (
                    int("".join(filter(str.isdigit, price_text))) if price_text else 0
                )
                views = None
                data.append((item_id, seller_id, price, views))
            browser.close()

        with Session(self.engine) as session:
            for item_id, seller_id, price, views in data:
                comp_item = session.scalar(
                    select(CompetitorItem).where(CompetitorItem.item_id == item_id)
                )
                if not comp_item:
                    comp_item = CompetitorItem(
                        item_id=item_id, seller_id=seller_id, price=price, views=views
                    )
                    session.add(comp_item)
                    session.flush()
                else:
                    comp_item.price = price
                    comp_item.last_seen = dt.datetime.utcnow()
                    comp_item.views = views
                session.add(CompetitorView(item_id=comp_item.id, views=views or 0))
            session.commit()
