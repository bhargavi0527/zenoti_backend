"""Add service_code to services

Revision ID: c2104a0c686b
Revises: 996a43d18cd9
Create Date: 2025-08-29 17:43:17.577227

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = 'c2104a0c686b'
down_revision: Union[str, Sequence[str], None] = '996a43d18cd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add column as nullable first
    op.add_column('services', sa.Column('service_code', sa.String(), nullable=True))

    # 2. Populate existing rows with generated codes
    conn = op.get_bind()
    results = conn.execute(sa.text("SELECT id FROM services")).fetchall()
    for row in results:
        code = f"SERV{str(uuid.uuid4().int)[:6]}"  # Example: SERV123456
        conn.execute(
            sa.text("UPDATE services SET service_code = :code WHERE id = :id"),
            {"code": code, "id": row.id},
        )

    # 3. Alter column to be non-nullable
    op.alter_column('services', 'service_code', nullable=False)

    # 4. Create unique index
    op.create_index(op.f('ix_services_service_code'), 'services', ['service_code'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_services_service_code'), table_name='services')
    op.drop_column('services', 'service_code')
