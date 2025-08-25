"""drop appointment_date from appointments

Revision ID: 0bb93904616e
Revises: b4d214af16f1
Create Date: 2025-08-25 13:46:02.771000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bb93904616e'
down_revision: Union[str, Sequence[str], None] = 'b4d214af16f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
