"""fix last migrations in images

Revision ID: dcbfb57f083b
Revises: 0b997959aef0
Create Date: 2023-09-08 20:32:22.603283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcbfb57f083b'
down_revision: Union[str, None] = '0b997959aef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'edited_cloudinary_url',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'edited_cloudinary_url',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    # ### end Alembic commands ###
