"""re-add appointment_date to appointments

Revision ID: f96ca071c754
Revises: a458cd4d6b20
Create Date: 2025-08-25 14:09:30.182347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f96ca071c754'
down_revision: Union[str, Sequence[str], None] = 'a458cd4d6b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('appointments', sa.Column('appointment_date', sa.Date, nullable=False))

def downgrade():
    op.drop_column('appointments', 'appointment_date')