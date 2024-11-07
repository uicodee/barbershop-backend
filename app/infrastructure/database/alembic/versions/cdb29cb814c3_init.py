"""init

Revision ID: cdb29cb814c3
Revises: 40b4a9e03132
Create Date: 2024-11-06 22:59:43.873983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdb29cb814c3'
down_revision = '40b4a9e03132'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('employee_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'client', 'employee', ['employee_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'client', type_='foreignkey')
    op.drop_column('client', 'employee_id')
    # ### end Alembic commands ###
