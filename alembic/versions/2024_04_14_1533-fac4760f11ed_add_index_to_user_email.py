"""Add index to user email

Revision ID: fac4760f11ed
Revises: b4e646026dac
Create Date: 2024-04-14 15:33:39.832752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac4760f11ed'
down_revision: Union[str, None] = 'b4e646026dac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    # ### end Alembic commands ###
