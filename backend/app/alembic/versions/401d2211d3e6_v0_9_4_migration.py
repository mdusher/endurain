"""v0.9.4 migration

Revision ID: 401d2211d3e6
Revises: 7217cc0eee8c
Create Date: 2025-04-05 06:20:15.064014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '401d2211d3e6'
down_revision: Union[str, None] = '7217cc0eee8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('health_data', sa.Column('vo2max', sa.DECIMAL(precision=10, scale=2), nullable=True, comment='Garmin Connect Precise vo2Max'))


def downgrade() -> None:
    op.drop_column('health_data', 'vo2max')

