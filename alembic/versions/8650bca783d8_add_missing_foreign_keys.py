"""Add missing foreign keys

Revision ID: 8650bca783d8
Revises: 1affd2fb4df9
Create Date: 2025-09-02 15:37:01.986765
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8650bca783d8'
down_revision: Union[str, Sequence[str], None] = '1affd2fb4df9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema safely."""
    # Add foreign key to appointments.center_id if it doesn't exist
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint WHERE conname = 'appointments_center_id_fkey'
        ) THEN
            ALTER TABLE appointments
            ADD CONSTRAINT appointments_center_id_fkey
            FOREIGN KEY(center_id) REFERENCES centers(id);
        END IF;
    END $$;
    """)

    # You can add similar DO $$ blocks for other FKs if needed
    # Example for provider_id:
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint WHERE conname = 'appointments_provider_id_fkey'
        ) THEN
            ALTER TABLE appointments
            ADD CONSTRAINT appointments_provider_id_fkey
            FOREIGN KEY(provider_id) REFERENCES providers(id);
        END IF;
    END $$;
    """)


def downgrade() -> None:
    """Downgrade schema safely."""
    op.execute("""
    ALTER TABLE appointments DROP CONSTRAINT IF EXISTS appointments_center_id_fkey;
    """)
    op.execute("""
    ALTER TABLE appointments DROP CONSTRAINT IF EXISTS appointments_provider_id_fkey;
    """)
