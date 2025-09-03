"""alter provider_id type to UUID and add foreign key in appointments

Revision ID: 27b88439ed69
Revises: bc93ca966887
Create Date: 2025-09-02 15:09:44.833848
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '27b88439ed69'
down_revision: Union[str, Sequence[str], None] = 'bc93ca966887'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade appointments.provider_id to UUID with foreign key."""
    # Drop old FK if it exists
    op.execute("""
        ALTER TABLE appointments
        DROP CONSTRAINT IF EXISTS appointments_provider_id_fkey
    """)

    # Alter column type to UUID
    op.alter_column(
        'appointments',
        'provider_id',
        type_=postgresql.UUID(),
        existing_type=sa.String(length=50),  # adjust if previous type was different
        postgresql_using="provider_id::uuid",
        nullable=False
    )

    # Add foreign key
    op.create_foreign_key(
        "appointments_provider_id_fkey",
        "appointments",
        "providers",
        ["provider_id"],
        ["id"]
    )


def downgrade():
    """Revert appointments.provider_id back to previous type."""
    # Drop FK
    op.execute("""
        ALTER TABLE appointments
        DROP CONSTRAINT IF EXISTS appointments_provider_id_fkey
    """)

    # Alter column type back (adjust type if it was different)
    op.alter_column(
        'appointments',
        'provider_id',
        type_=sa.String(length=50),
        existing_type=postgresql.UUID(),
        postgresql_using="provider_id::text",
        nullable=True
    )
