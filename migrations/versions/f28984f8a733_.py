"""empty message

Revision ID: f28984f8a733
Revises: be1b6c5fa3ae
Create Date: 2020-12-15 16:09:46.562992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f28984f8a733'
down_revision = 'be1b6c5fa3ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('code', sa.String(length=20), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_code'), 'team', ['code'], unique=True)
    op.create_table('staffteam',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_staffteam_staff_id'), 'staffteam', ['staff_id'], unique=True)
    op.add_column('staff', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('staff', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_index('ix_staff_status', table_name='staff')
    op.create_foreign_key(None, 'staff', 'staff', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff', type_='foreignkey')
    op.create_index('ix_staff_status', 'staff', ['status'], unique=False)
    op.drop_column('staff', 'parent_id')
    op.drop_column('staff', 'is_superuser')
    op.drop_index(op.f('ix_staffteam_staff_id'), table_name='staffteam')
    op.drop_table('staffteam')
    op.drop_index(op.f('ix_team_code'), table_name='team')
    op.drop_table('team')
    # ### end Alembic commands ###