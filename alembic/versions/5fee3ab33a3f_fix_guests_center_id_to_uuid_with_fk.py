"""fix guests.center_id to UUID with FK

Revision ID: 5fee3ab33a3f
Revises: d3bcbc5f340b
Create Date: 2025-09-02 12:46:47.422341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fee3ab33a3f'
down_revision: Union[str, Sequence[str], None] = 'd3bcbc5f340b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Cast VARCHAR → UUID safely
    op.alter_column(
        'guests',
        'center_id',
        existing_type=sa.VARCHAR(),
        type_=sa.UUID(),
        existing_nullable=False,
        postgresql_using="center_id::uuid"   # 👈 explicit cast
    )

    # Add foreign key to centers.id
    op.create_foreign_key(
        "guests_center_id_fkey",   # 👈 give the FK a name
        "guests",
        "centers",
        ["center_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("guests_center_id_fkey", "guests", type_="foreignkey")
    op.alter_column(
        "guests",
        "center_id",
        existing_type=sa.UUID(),
        type_=sa.VARCHAR(),
        existing_nullable=False
    )
