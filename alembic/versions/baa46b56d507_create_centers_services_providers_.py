import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'baa46b56d507'
down_revision: str = 'a67e7536ff5c'
branch_labels = None
depends_on = None

# Define Enum once
appointment_status_enum = sa.Enum(
    'scheduled', 'confirmed', 'completed', 'cancelled', 'no_show',
    name='appointmentstatus'
)

def upgrade() -> None:
    """Upgrade schema."""

    # --- Create dependent tables first ---
    op.create_table(
        'centers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_centers_id'), 'centers', ['id'], unique=False)

    op.create_table(
        'services',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)

    op.create_table(
        'providers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('specialization', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('center_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['center_id'], ['centers.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_providers_email'), 'providers', ['email'], unique=True)
    op.create_index(op.f('ix_providers_id'), 'providers', ['id'], unique=False)

    # --- Create Enum type in DB ---
    appointment_status_enum.create(op.get_bind(), checkfirst=True)

    # --- Appointments table modifications ---
    op.add_column('appointments', sa.Column('provider_id', sa.UUID(), nullable=False))
    op.add_column('appointments', sa.Column('service_id', sa.UUID(), nullable=False))
    op.add_column('appointments', sa.Column('notes', sa.Text(), nullable=True))

    # Convert center_id safely to UUID
    op.alter_column(
        'appointments',
        'center_id',
        existing_type=sa.VARCHAR(),
        type_=sa.UUID(),
        existing_nullable=False,
        postgresql_using="center_id::uuid"
    )

    # Convert status safely to Enum
    op.execute(
        "ALTER TABLE appointments ALTER COLUMN status TYPE appointmentstatus USING status::text::appointmentstatus"
    )

    # Create foreign keys
    op.create_foreign_key(None, 'appointments', 'providers', ['provider_id'], ['id'])
    op.create_foreign_key(None, 'appointments', 'centers', ['center_id'], ['id'])
    op.create_foreign_key(None, 'appointments', 'services', ['service_id'], ['id'])

    # Drop old columns
    op.drop_column('appointments', 'center_name')
    op.drop_column('appointments', 'service_name')


def downgrade() -> None:
    """Downgrade schema."""

    # Re-add old columns
    op.add_column('appointments', sa.Column('service_name', sa.VARCHAR(), nullable=False))
    op.add_column('appointments', sa.Column('center_name', sa.VARCHAR(), nullable=False))

    # Drop foreign keys
    op.drop_constraint(None, 'appointments', type_='foreignkey')
    op.drop_constraint(None, 'appointments', type_='foreignkey')
    op.drop_constraint(None, 'appointments', type_='foreignkey')

    # Convert status back to VARCHAR
    op.alter_column(
        'appointments',
        'status',
        existing_type=appointment_status_enum,
        type_=sa.VARCHAR(),
        nullable=True
    )

    # Convert center_id back to VARCHAR
    op.alter_column(
        'appointments',
        'center_id',
        existing_type=sa.UUID(),
        type_=sa.VARCHAR(),
        existing_nullable=False
    )

    # Drop added columns
    op.drop_column('appointments', 'notes')
    op.drop_column('appointments', 'service_id')
    op.drop_column('appointments', 'provider_id')

    # Drop created tables and indexes
    op.drop_index(op.f('ix_providers_id'), table_name='providers')
    op.drop_index(op.f('ix_providers_email'), table_name='providers')
    op.drop_table('providers')

    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')

    op.drop_index(op.f('ix_centers_id'), table_name='centers')
    op.drop_table('centers')

    # Drop Enum type
    appointment_status_enum.drop(op.get_bind(), checkfirst=True)
