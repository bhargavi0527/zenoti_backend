"""fix appointment model foreign keys to use UUID

Revision ID: bc93ca966887
Revises: 5fee3ab33a3f
Create Date: 2025-09-02 14:29:02.939921
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc93ca966887'
down_revision: Union[str, Sequence[str], None] = '5fee3ab33a3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade appointments.provider_id to UUID with FK."""
    # Drop old FK if it exists
    op.execute("""
        ALTER TABLE appointments
        DROP CONSTRAINT IF EXISTS appointments_provider_id_fkey
    """)

    # Ensure provider_id column is UUID (no conversion to integer)
    op.alter_column(
        "appointments",
        "provider_id",
        type_=postgresql.UUID(),
        existing_type=sa.String(length=50),  # adjust if needed
        postgresql_using="provider_id::uuid",
        nullable=False
    )

    # Create foreign key
    op.create_foreign_key(
        "appointments_provider_id_fkey",
        "appointments",
        "providers",
        ["provider_id"],
        ["id"]
    )


def downgrade() -> None:
    """Revert appointments.provider_id (keep as string for safety)."""
    # Drop FK if it exists
    op.execute("""
        ALTER TABLE appointments
        DROP CONSTRAINT IF EXISTS appointments_provider_id_fkey
    """)

    # Revert column type back to string
    op.alter_column(
        "appointments",
        "provider_id",
        type_=sa.String(length=50),
        existing_type=postgresql.UUID(),
        postgresql_using="provider_id::text",
        nullable=True
    )
