"""Service for description synchronization."""

from __future__ import annotations

from ..core.avito_client import AvitoClient


class DescriptionService:
    def __init__(self, client: AvitoClient, account_id: str) -> None:
        self.client = client
        self.account_id = account_id

    def update_all_items(self, text: str) -> None:
        items = self.client.get_items_stats(self.account_id)
        for item in items:
            self.client.update_description(self.account_id, str(item["item_id"]), text)
