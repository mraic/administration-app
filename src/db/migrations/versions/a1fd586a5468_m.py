"""-m

Revision ID: a1fd586a5468
Revises: d10fb2bab49a
Create Date: 2022-06-30 13:05:46.486246

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1fd586a5468'
down_revision = 'd10fb2bab49a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lists',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='ck_modellist_status', native_enum=False, create_constraint=True, length=255), server_default='active', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lists'))
    )
    op.create_table('listitems',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='ck_modellist_status', native_enum=False, create_constraint=True, length=255), server_default='active', nullable=False),
    sa.Column('list_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['list_id'], ['lists.id'], name=op.f('fk_listitems_list_id'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_listitems'))
    )
    op.create_index(op.f('ix_listitems_list_id'), 'listitems', ['list_id'], unique=False)
    op.add_column('items', sa.Column('listitems_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f('ix_items_listitems_id'), 'items', ['listitems_id'], unique=False)
    op.create_foreign_key(op.f('fk_items_listitems_id'), 'items', 'listitems', ['listitems_id'], ['id'], ondelete='RESTRICT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_items_listitems_id'), 'items', type_='foreignkey')
    op.drop_index(op.f('ix_items_listitems_id'), table_name='items')
    op.drop_column('items', 'listitems_id')
    op.drop_index(op.f('ix_listitems_list_id'), table_name='listitems')
    op.drop_table('listitems')
    op.drop_table('lists')
    # ### end Alembic commands ###