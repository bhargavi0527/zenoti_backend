"""add foreign keys to appointments

Revision ID: 1affd2fb4df9
Revises: 27b88439ed69
Create Date: 2025-09-02 15:24:38.462377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1affd2fb4df9'
down_revision: Union[str, Sequence[str], None] = '27b88439ed69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ Add foreign key to guests if not exists
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'appointments_guest_id_fkey'
        ) THEN
            ALTER TABLE appointments
            ADD CONSTRAINT appointments_guest_id_fkey
            FOREIGN KEY (guest_id) REFERENCES guests(id);
        END IF;
    END
    $$;
    """)

    # ✅ Add foreign key to services if not exists
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'appointments_service_id_fkey'
        ) THEN
            ALTER TABLE appointments
            ADD CONSTRAINT appointments_service_id_fkey
            FOREIGN KEY (service_id) REFERENCES services(id);
        END IF;
    END
    $$;
    """)


def downgrade():
    # Drop foreign keys safely
    op.execute("ALTER TABLE appointments DROP CONSTRAINT IF EXISTS appointments_service_id_fkey;")
    op.execute("ALTER TABLE appointments DROP CONSTRAINT IF EXISTS appointments_guest_id_fkey;")
