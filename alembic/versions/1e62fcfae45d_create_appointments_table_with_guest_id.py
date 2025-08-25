"""create appointments table with guest_id

Revision ID: 1e62fcfae45d
Revises: 5ee2881ccfdd
Create Date: 2025-08-25 12:17:10.118462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e62fcfae45d'
down_revision: Union[str, Sequence[str], None] = '5ee2881ccfdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
