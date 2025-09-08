"""add default generator in sales and invoice tables

Revision ID: 92892f443867
Revises: f9525d54d809
Create Date: 2025-09-04 17:54:00.382426
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '92892f443867'
down_revision = 'f9525d54d809'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""

    # Add server_default for sale_no in sales table (optional, if you want DB to generate)
    op.alter_column(
        'sales',
        'sale_no',
        existing_type=sa.String(),
        nullable=False,
        server_default=sa.text("'SALE-' || substring(md5(random()::text), 1, 8)")
    )

    # Add server_default for invoice_no in invoices table (optional)
    op.alter_column(
        'invoices',
        'invoice_no',
        existing_type=sa.String(),
        nullable=False,
        server_default=sa.text("'INV-' || substring(md5(random()::text), 1, 8)")
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove server defaults
    op.alter_column('sales', 'sale_no', server_default=None)
    op.alter_column('invoices', 'invoice_no', server_default=None)
