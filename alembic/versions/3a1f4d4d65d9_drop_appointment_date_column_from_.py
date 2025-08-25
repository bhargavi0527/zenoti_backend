"""drop appointment_date column from appointments

Revision ID: 3a1f4d4d65d9
Revises: 0bb93904616e
Create Date: 2025-08-25 14:00:58.606592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a1f4d4d65d9'
down_revision: Union[str, Sequence[str], None] = 'b4d214af16f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("appointments") as batch_op:
        batch_op.drop_column("appointment_date")

def downgrade():
    with op.batch_alter_table("appointments") as batch_op:
        batch_op.add_column(
            sa.Column("appointment_date", sa.DateTime(timezone=True), nullable=False)
        )