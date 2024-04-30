"""add quantity attr from Order table

Revision ID: 1284c3083a5f
Revises: cde56ba7bff5
Create Date: 2024-04-29 16:51:48.580662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1284c3083a5f'
down_revision: Union[str, None] = 'cde56ba7bff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    op.add_column('orders', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
