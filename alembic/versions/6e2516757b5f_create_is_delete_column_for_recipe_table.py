"""Create is delete column for recipe table

Revision ID: 6e2516757b5f
Revises: 
Create Date: 2026-04-21 12:34:45.980125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e2516757b5f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # user server_default for data base level  set defualt value for previous generated data  
    op.add_column('recipes',sa.Column('is_deleted',sa.Boolean,nullable=False,server_default=sa.false()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('recipes','is_deleted')
