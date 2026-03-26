"""add token slug and backfill

Revision ID: f5347ef63ae6
Revises: f18364e61213
Create Date: 2026-03-24 12:41:57.468381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
import secrets
import string

# revision identifiers, used by Alembic.
revision: str = 'f5347ef63ae6'
down_revision: Union[str, Sequence[str], None] = 'f18364e61213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ALPHABET = string.ascii_letters + string.digits

def generate_slug(length: int = 10) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("tokens", sa.Column("slug", sa.String(length=32), nullable=True))
    conn = op.get_bind()
    rows = conn.execute(text("SELECT id FROM tokens WHERE slug IS NULL")).fetchall()
    used_slugs = set()

    existing = conn.execute(text("SELECT slug FROM tokens WHERE slug IS NOT NULL")).fetchall()
    used_slugs.update(row[0] for row in existing if row[0])

    for row in rows:
        token_id = row[0]
        slug = generate_slug()

        while slug in used_slugs:
            slug = generate_slug()

        used_slugs.add(slug)

        conn.execute(
            text(
                """
                UPDATE tokens
                SET slug = :slug
                WHERE id = :token_id
                """
            ),
            {"slug": slug, "token_id": token_id}
        )

    op.create_unique_constraint("uq_tokens_slug", "tokens", ["slug"])
    op.alter_column("tokens", "slug", existing_type=sa.String(length=32), nullable=False)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_tokens_slug", "tokens", type_="unique")
    op.drop_column("tokens", "slug")
    pass
