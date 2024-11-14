"""init

Revision ID: 8f1b09672f2a
Revises: fb472a69c9eb
Create Date: 2024-11-14 23:46:09.548065

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8f1b09672f2a'
down_revision = 'fb472a69c9eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Добавляем новый столбец с значением по умолчанию
    op.add_column('client', sa.Column('period', sa.Integer(), server_default='30', nullable=False))

    # Обновляем уже существующие записи, где значение period = NULL
    op.execute("UPDATE client SET period = 30 WHERE period IS NULL")

    # Убираем server_default после обновления данных
    op.alter_column('client', 'period', server_default=None)


def downgrade() -> None:
    # Удаляем столбец 'period' при откате
    op.drop_column('client', 'period')
