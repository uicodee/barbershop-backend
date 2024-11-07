"""init

Revision ID: 40b4a9e03132
Revises: d9e3528391c6
Create Date: 2024-11-06 22:31:39.071956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40b4a9e03132'
down_revision = 'd9e3528391c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('branch_id', sa.BigInteger(), nullable=False))
    op.add_column('appointment', sa.Column('employee_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'appointment', 'employee', ['employee_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'appointment', 'branch', ['branch_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'appointment', type_='foreignkey')
    op.drop_constraint(None, 'appointment', type_='foreignkey')
    op.drop_column('appointment', 'employee_id')
    op.drop_column('appointment', 'branch_id')
    # ### end Alembic commands ###
