"""add scheduled_time to appointments

Revision ID: b4d214af16f1
Revises: 1e62fcfae45d
Create Date: 2025-08-25 13:37:16.591070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4d214af16f1'
down_revision: Union[str, Sequence[str], None] = '1e62fcfae45d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "appointments",
        sa.Column("scheduled_time", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_column("appointments", "scheduled_time")
