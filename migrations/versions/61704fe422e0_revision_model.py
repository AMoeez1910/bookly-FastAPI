"""revision model

Revision ID: 61704fe422e0
Revises: 2a88729dbd5d
Create Date: 2025-07-15 17:19:27.774967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '61704fe422e0'
down_revision: Union[str, Sequence[str], None] = '2a88729dbd5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('book_uid', sa.Uuid(), nullable=False),
    sa.Column('user_uid', sa.Uuid(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['book_uid'], ['books.uid'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_reviews_uid'), 'reviews', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reviews_uid'), table_name='reviews')
    op.drop_table('reviews')
    # ### end Alembic commands ###
