"""Added task table

Revision ID: 86914b7363ed
Revises: 
Create Date: 2025-06-30 12:23:19.532251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86914b7363ed'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'task',
        sa.Column('id', sa.Integer()),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.VARCHAR(200)),
        sa.Column('status', sa.VARCHAR(200)),
        sa.Column('due_date', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("task")
    pass
    # ### end Alembic commands ###
