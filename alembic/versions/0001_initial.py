"""Initial tables"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "item_stats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("item_id", sa.String, nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("views", sa.Integer, nullable=False),
    )
    op.create_table(
        "competitor_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("item_id", sa.String, nullable=False),
        sa.Column("seller_id", sa.String, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("last_seen", sa.DateTime, nullable=False),
        sa.Column("views", sa.Integer),
    )
    op.create_table(
        "competitor_views",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "item_id", sa.Integer, sa.ForeignKey("competitor_items.id"), nullable=False
        ),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column("views", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("competitor_views")
    op.drop_table("competitor_items")
    op.drop_table("item_stats")
