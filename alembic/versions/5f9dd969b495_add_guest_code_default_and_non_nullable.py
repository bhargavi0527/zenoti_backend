"""add guest_code default and non-nullable

Revision ID: 5f9dd969b495
Revises: 8aa747aea0b3
Create Date: 2025-08-28 16:35:03.431780
"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '5f9dd969b495'
down_revision = '8aa747aea0b3'
branch_labels = None
depends_on = None

# Function to generate a random guest code
def generate_guest_code():
    return f"GUEST{str(uuid.uuid4().int)[:6]}"

def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    # Fill existing NULL guest_code values
    guests = connection.execute(sa.text("SELECT id FROM guests WHERE guest_code IS NULL")).fetchall()
    for guest in guests:
        code = generate_guest_code()
        connection.execute(
            sa.text("UPDATE guests SET guest_code = :code WHERE id = :id"),
            {"code": code, "id": str(guest.id)}
        )

    # Now safely alter the column to NOT NULL
    op.alter_column('guests', 'guest_code',
                    existing_type=sa.VARCHAR(),
                    nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('guests', 'guest_code',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
