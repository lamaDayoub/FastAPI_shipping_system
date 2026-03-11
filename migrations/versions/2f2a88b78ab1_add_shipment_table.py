"""add shipment table

Revision ID: 2f2a88b78ab1
Revises: 
Create Date: 2026-03-11 12:12:05.576643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2a88b78ab1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shipment",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("content", sa.CHAR, nullable= False),
        sa.Column("status", sa.CHAR, nullable= False),
    )


def downgrade() -> None:
    op.drop_table("shipment")
