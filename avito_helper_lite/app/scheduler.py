"""Scheduler configuration."""

from __future__ import annotations

import os
from datetime import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from .core.avito_client import AvitoClient
from .services.competitor_service import CompetitorService
from .services.stats_service import StatsService


def create_scheduler() -> BackgroundScheduler:
    db_url = os.getenv("DATABASE_URL", "")
    jobstores = {"default": SQLAlchemyJobStore(url=db_url)}
    scheduler = BackgroundScheduler(jobstores=jobstores, timezone="Europe/Moscow")

    client = AvitoClient(
        os.getenv("AVITO_CLIENT_ID", ""),
        os.getenv("AVITO_CLIENT_SECRET", ""),
        os.getenv("AVITO_REFRESH_TOKEN", ""),
    )
    account_id = os.getenv("ACCOUNT_ID", "")

    stats_service = StatsService(client, account_id, db_url)
    competitor_service = CompetitorService(db_url)

    scheduler.add_job(
        stats_service.collect_daily_views,
        "cron",
        hour=23,
        minute=0,
        id="collect_daily_views",
        replace_existing=True,
    )
    scheduler.add_job(
        competitor_service.track,
        "cron",
        hour=0,
        minute=30,
        id="competitor_tracker",
        replace_existing=True,
    )

    return scheduler
