"""init

Revision ID: 1df6ae21a0e5
Revises: 48e52d9c7b2f
Create Date: 2024-11-02 13:00:05.803725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1df6ae21a0e5'
down_revision = '48e52d9c7b2f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('branch_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'employee', 'branch', ['branch_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.drop_column('employee', 'branch_id')
    # ### end Alembic commands ###
