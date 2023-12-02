"""empty message

Revision ID: de58890c1800
Revises: 
Create Date: 2023-11-30 13:16:41.662873

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from services.db.enums import UserRole

# revision identifiers, used by Alembic.
revision: str = 'de58890c1800'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('language_code', sa.String(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('role', sa.Enum('ADMIN', 'USER', 'GUEST', name='userrole'), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('credentials',
                    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
                    sa.Column('password', sa.String(length=64), nullable=False),
                    sa.Column('master_password', sa.String(length=64), nullable=False),
                    sa.Column('salt', sa.LargeBinary(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('records',
                    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
                    sa.Column('title', sa.String(length=64), nullable=False),
                    sa.Column('username', sa.LargeBinary(), nullable=False),
                    sa.Column('password', sa.LargeBinary(), nullable=False),
                    sa.Column('salt', sa.LargeBinary(), nullable=False),
                    sa.Column('url', sa.String(length=64), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('comments',
                    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
                    sa.Column('text', sa.String(length=256), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('record_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['record_id'], ['records.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('records')
    op.drop_table('credentials')
    op.drop_table('users')

    role = sa.Enum(UserRole, name='userrole')
    role.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
