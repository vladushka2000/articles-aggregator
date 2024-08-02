"""fill_article_topic_table

Revision ID: 08fbce1e3022
Revises: b97c1e7fd6df
Create Date: 2024-07-28 16:15:13.438802

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from tools import enums

# revision identifiers, used by Alembic.
revision: str = "08fbce1e3022"
down_revision: Union[str, None] = "b97c1e7fd6df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind(), only=("article_topic",))

    article_topic_table = sa.Table("article_topic", meta)

    topics = [{"id": topic.id, "name": topic.value} for topic in enums.ArticleTopic]

    op.execute("TRUNCATE TABLE article_topic CASCADE")
    op.bulk_insert(article_topic_table, topics)


def downgrade() -> None:
    op.execute("TRUNCATE TABLE article_topic CASCADE")
