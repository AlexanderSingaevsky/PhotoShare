"""add_permissions_table

Revision ID: d0488da942da
Revises: dcb5e976290e
Create Date: 2023-09-02 20:50:32.831885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = 'd0488da942da'
down_revision: Union[str, None] = 'dcb5e976290e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permissions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('role_name', sa.String(length=20), nullable=False),
                    sa.Column('can_add_image', sa.Boolean(), nullable=False),
                    sa.Column('can_update_image', sa.Boolean(), nullable=False),
                    sa.Column('can_delete_image', sa.Boolean(), nullable=False),
                    sa.Column('can_add_tag', sa.Boolean(), nullable=False),
                    sa.Column('can_update_tag', sa.Boolean(), nullable=False),
                    sa.Column('can_delete_tag', sa.Boolean(), nullable=False),
                    sa.Column('can_add_comment', sa.Boolean(), nullable=False),
                    sa.Column('can_update_comment', sa.Boolean(), nullable=False),
                    sa.Column('can_delete_comment', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('role_name')
                    )
    op.create_foreign_key(None, 'user', 'permissions', ['access_level'], ['id'])

    permissions_temp_table = table('permissions',
                                   column('id', sa.Integer),
                                   column('role_name', sa.String),
                                   column('can_add_image', sa.Boolean),
                                   column('can_update_image', sa.Boolean),
                                   column('can_delete_image', sa.Boolean),
                                   column('can_add_tag', sa.Boolean),
                                   column('can_update_tag', sa.Boolean),
                                   column('can_delete_tag', sa.Boolean),
                                   column('can_add_comment', sa.Boolean),
                                   column('can_update_comment', sa.Boolean),
                                   column('can_delete_comment', sa.Boolean)
                                   )

    op.bulk_insert(permissions_temp_table, [
        {
            "id": 1,
            "role_name": "User",
            "can_add_image": True,
            "can_update_image": False,
            "can_delete_image": False,
            "can_add_tag": True,
            "can_update_tag": False,
            "can_delete_tag": False,
            "can_add_comment": True,
            "can_update_comment": False,
            "can_delete_comment": False
        },
        {
            "id": 2,
            "role_name": "Moderator",
            "can_add_image": True,
            "can_update_image": False,
            "can_delete_image": True,
            "can_add_tag": True,
            "can_update_tag": True,
            "can_delete_tag": True,
            "can_add_comment": True,
            "can_update_comment": True,
            "can_delete_comment": False
        },
        {
            "id": 3,
            "role_name": "Admin",
            "can_add_image": True,
            "can_update_image": True,
            "can_delete_image": True,
            "can_add_tag": True,
            "can_update_tag": True,
            "can_delete_tag": True,
            "can_add_comment": True,
            "can_update_comment": True,
            "can_delete_comment": True
        }
    ])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_table('permissions')
    # ### end Alembic commands ###
