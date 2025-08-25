"""merge multiple heads

Revision ID: a458cd4d6b20
Revises: 0bb93904616e, 3a1f4d4d65d9
Create Date: 2025-08-25 14:04:57.325142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a458cd4d6b20'
down_revision: Union[str, Sequence[str], None] = ('0bb93904616e', '3a1f4d4d65d9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
