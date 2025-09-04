"""added fields in user model

Revision ID: 9fe983ec9df7
Revises: 8650bca783d8
Create Date: 2025-09-04 11:00:10.549511

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fe983ec9df7'
down_revision: Union[str, Sequence[str], None] = '8650bca783d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add new columns as nullable=True
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)

    # Step 2: (Optional) backfill existing rows if any
    # op.execute("UPDATE users SET first_name='Temp', last_name='User', phone_number='0000000000' WHERE first_name IS NULL")

    # Step 3: Make columns NOT NULL
    op.alter_column('users', 'first_name', nullable=False)
    op.alter_column('users', 'last_name', nullable=False)
    op.alter_column('users', 'phone_number', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
