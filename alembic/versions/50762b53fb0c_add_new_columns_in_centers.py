"""add new columns in centers

Revision ID: 50762b53fb0c
Revises: e8ed5f17bf40
Create Date: 2025-08-28 11:14:39.181910
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '50762b53fb0c'
down_revision: Union[str, Sequence[str], None] = 'e8ed5f17bf40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Step 1: Add code column as nullable first
    op.add_column('centers', sa.Column('code', sa.String(), nullable=True))
    op.add_column('centers', sa.Column('display_name', sa.String(), nullable=True))
    op.add_column('centers', sa.Column('country', sa.String(), nullable=True))
    op.add_column('centers', sa.Column('state', sa.String(), nullable=True))
    op.add_column('centers', sa.Column('contact_info_phone', sa.String(), nullable=True))
    op.add_column('centers', sa.Column('contact_info_email', sa.String(), nullable=True))

    # Step 2: Backfill existing rows with safe defaults
    op.execute("UPDATE centers SET code = 'TEMP_CODE_' || id::text WHERE code IS NULL")
    op.execute("UPDATE centers SET display_name = name WHERE display_name IS NULL")

    # Step 3: Alter code column to be NOT NULL
    op.alter_column('centers', 'code', nullable=False)

    # Step 4: Add unique constraint on code
    op.create_unique_constraint("uq_centers_code", 'centers', ['code'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_centers_code", 'centers', type_='unique')
    op.drop_column('centers', 'contact_info_email')
    op.drop_column('centers', 'contact_info_phone')
    op.drop_column('centers', 'state')
    op.drop_column('centers', 'country')
    op.drop_column('centers', 'display_name')
    op.drop_column('centers', 'code')
