"""14_03_2021 migration_2

Revision ID: 98cf70e48234
Revises: 2baeef77aa27
Create Date: 2021-03-14 13:06:57.543197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98cf70e48234'
down_revision = '2baeef77aa27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('change_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_type', sa.String(length=100), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum('create', 'update', 'delete', name='changeactions'), nullable=False),
    sa.Column('field', sa.String(length=100), nullable=True),
    sa.Column('old_value', sa.String(), nullable=True),
    sa.Column('new_value', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_change_history_entity_id'), 'change_history', ['entity_id'], unique=False)
    op.alter_column('applications', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('environments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('variables', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('variables', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('environments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('applications', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_index(op.f('ix_change_history_entity_id'), table_name='change_history')
    op.drop_table('change_history')
    # ### end Alembic commands ###
