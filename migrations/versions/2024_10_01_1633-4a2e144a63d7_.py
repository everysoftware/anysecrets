"""empty message

Revision ID: 4a2e144a63d7
Revises: 46345c9de87d
Create Date: 2024-10-01 16:33:35.244057

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4a2e144a63d7"
down_revision: Union[str, None] = "46345c9de87d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("__test_waffles__")
    op.add_column("passwords", sa.Column("name", sa.String(), nullable=False))
    op.add_column(
        "passwords",
        sa.Column("encrypted_username", sa.String(), nullable=False),
    )
    op.add_column(
        "passwords",
        sa.Column("encrypted_password", sa.String(), nullable=False),
    )
    op.drop_column("passwords", "username")
    op.drop_column("passwords", "password")
    op.drop_column("passwords", "title")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "passwords",
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "passwords",
        sa.Column(
            "password", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "passwords",
        sa.Column(
            "username", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("passwords", "encrypted_password")
    op.drop_column("passwords", "encrypted_username")
    op.drop_column("passwords", "name")
    op.create_table(
        "__test_waffles__",
        sa.Column(
            "id",
            sa.BIGINT(),
            sa.Identity(
                always=False,
                start=1,
                increment=1,
                minvalue=1,
                maxvalue=9223372036854775807,
                cycle=False,
                cache=1,
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("age", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="__test_waffles___pkey"),
    )
    # ### end Alembic commands ###
