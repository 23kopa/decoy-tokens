"""drop token secret_hash

Revision ID: 3964fb20af0c
Revises: f5347ef63ae6
Create Date: 2026-03-24 13:19:46.836806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3964fb20af0c'
down_revision: Union[str, Sequence[str], None] = 'f5347ef63ae6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("tokens", "secret_hash")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "tokens",
        sa.Column("secret_hash", sa.String(length=128), nullable=True)
    )
    pass
