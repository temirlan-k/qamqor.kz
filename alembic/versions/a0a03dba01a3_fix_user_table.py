"""fix user table

Revision ID: a0a03dba01a3
Revises: 4bfe59221dde
Create Date: 2024-04-14 07:26:03.915515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0a03dba01a3'
down_revision: Union[str, None] = '4bfe59221dde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_index('ix_users_slug', table_name='users')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'slug')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.create_index('ix_users_slug', 'users', ['slug'], unique=True)
    op.drop_column('users', 'is_verified')
    # ### end Alembic commands ###
