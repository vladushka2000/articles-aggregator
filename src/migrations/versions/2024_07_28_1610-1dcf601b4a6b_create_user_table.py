"""create_user_table

Revision ID: 1dcf601b4a6b
Revises: 
Create Date: 2024-07-28 16:10:27.972521

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1dcf601b4a6b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "id", sa.UUID(), nullable=False, comment="Идентификатор пользователя"
        ),
        sa.Column("name", sa.String(), nullable=True, comment="Имя пользователя"),
        sa.Column(
            "hashed_password", sa.String(), nullable=True, comment="Хешированный пароль"
        ),
        sa.Column(
            "registration_date",
            sa.DateTime(),
            nullable=True,
            comment="Дата регистрации",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
