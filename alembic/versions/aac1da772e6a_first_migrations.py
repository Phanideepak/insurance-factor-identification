"""first migrations

Revision ID: aac1da772e6a
Revises: 9bbcf6b55728
Create Date: 2024-10-21 11:51:49.233335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aac1da772e6a'
down_revision: Union[str, None] = '9bbcf6b55728'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
