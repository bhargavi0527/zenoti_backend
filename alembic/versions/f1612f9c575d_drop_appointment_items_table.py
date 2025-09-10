"""drop appointment_items table

Revision ID: f1612f9c575d
Revises: fc436b7ec431
Create Date: 2025-09-10 10:40:21.014043
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1612f9c575d'
down_revision: Union[str, Sequence[str], None] = 'fc436b7ec431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: drop table."""
    op.drop_index(op.f('ix_appointment_items_id'), table_name='appointment_items')
    op.drop_table('appointment_items')


def downgrade() -> None:
    """Downgrade schema: recreate table."""
    op.create_table(
        'appointment_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('discount', sa.Float(), nullable=True),
        sa.Column('net_price', sa.Float(), nullable=True),
        sa.Column('cashback_redemption', sa.Float(), nullable=True),
        sa.Column('appointment_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['appointment_id'], ['appointments.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointment_items_id'), 'appointment_items', ['id'], unique=False)
