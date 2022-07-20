"""Update_table_items

Revision ID: 6ace83f4205a
Revises: a1fd586a5468
Create Date: 2022-07-06 07:54:01.870354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6ace83f4205a'
down_revision = 'a1fd586a5468'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('condition_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.drop_index('ix_items_listitems_id', table_name='items')
    op.create_index(op.f('ix_items_condition_id'), 'items', ['condition_id'], unique=False)
    op.drop_constraint('fk_items_listitems_id', 'items', type_='foreignkey')
    op.create_foreign_key(op.f('fk_items_condition_id'), 'items', 'listitems', ['condition_id'], ['id'], ondelete='RESTRICT')
    op.drop_column('items', 'listitems_id')
    op.drop_column('items', 'condition')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('condition', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('items', sa.Column('listitems_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk_items_condition_id'), 'items', type_='foreignkey')
    op.create_foreign_key('fk_items_listitems_id', 'items', 'listitems', ['listitems_id'], ['id'], ondelete='RESTRICT')
    op.drop_index(op.f('ix_items_condition_id'), table_name='items')
    op.create_index('ix_items_listitems_id', 'items', ['listitems_id'], unique=False)
    op.drop_column('items', 'condition_id')
    # ### end Alembic commands ###