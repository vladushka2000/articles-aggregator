"""create_article_topic_table

Revision ID: b97c1e7fd6df
Revises: 1dcf601b4a6b
Create Date: 2024-07-28 16:13:05.233406

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b97c1e7fd6df"
down_revision: Union[str, None] = "1dcf601b4a6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "article_topic",
        sa.Column("id", sa.UUID(), nullable=False, comment="Идентификатор темы статьи"),
        sa.Column("name", sa.String(), nullable=True, comment="Название темы статьи"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("article_topic")
