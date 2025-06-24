"""Avito API client."""

from __future__ import annotations

import datetime as dt
import logging
from typing import Any

import requests
from requests import Response

logger = logging.getLogger(__name__)


class AvitoClient:
    BASE_URL = "https://api.avito.ru"
    OAUTH_URL = "https://api.avito.ru/token"

    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token: str | None = None
        self.token_expiry: dt.datetime | None = None

    def _refresh_token(self) -> None:
        logger.info("Refreshing access token")
        resp = requests.post(
            self.OAUTH_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data["access_token"]
        self.token_expiry = dt.datetime.utcnow() + dt.timedelta(
            seconds=data.get("expires_in", 3600)
        )

    def _auth_headers(self) -> dict[str, str]:
        if (
            not self.access_token
            or not self.token_expiry
            or dt.datetime.utcnow() >= self.token_expiry
        ):
            self._refresh_token()
        return {"Authorization": f"Bearer {self.access_token}"}

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        url = f"{self.BASE_URL}{path}"
        headers = kwargs.pop("headers", {})
        headers.update(self._auth_headers())
        resp = requests.request(method, url, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp

    def get_items_stats(self, account_id: str) -> list[dict[str, Any]]:
        resp = self.request("POST", f"/stats/v1/accounts/{account_id}/items")
        return resp.json().get("result", [])

    def update_description(self, account_id: str, item_id: str, text: str) -> None:
        self.request(
            "PUT",
            f"/core/v1/accounts/{account_id}/items/{item_id}",
            json={"description": text},
        )
