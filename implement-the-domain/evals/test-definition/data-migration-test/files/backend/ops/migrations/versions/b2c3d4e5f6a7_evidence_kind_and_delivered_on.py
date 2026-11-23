"""evidence kind and delivered_on

Revision ID: b2c3d4e5f6a7
Revises:
Create Date: 2026-09-01
"""

import sqlalchemy as sa
from alembic import op

revision = "b2c3d4e5f6a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evidence",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("procedure_id", sa.String, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("kind", sa.String, nullable=False),
        sa.Column("delivered_on", sa.Date, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("evidence")
