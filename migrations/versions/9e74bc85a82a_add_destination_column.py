"""add destination column

Revision ID: 9e74bc85a82a
Revises: 2f2a88b78ab1
Create Date: 2026-03-11 12:54:22.221261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e74bc85a82a'
down_revision: Union[str, Sequence[str], None] = '2f2a88b78ab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column("destination", sa.INTEGER, nullable = True)
    )


def downgrade() -> None:
    op.drop_column(
        "shipment",
        "destination"
    )
