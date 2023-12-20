"""DB Creation

Revision ID: 08d547648f4d
Revises: 
Create Date: 2023-12-20 10:43:07.608304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08d547648f4d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hash_key', sa.String(), nullable=False),
    sa.Column('auth_hash', sa.String(), nullable=False),
    sa.Column('priv_key', sa.String(), nullable=False),
    sa.Column('pub_key', sa.String(), nullable=False),
    sa.Column('avatar_path', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('login')
    )
    op.create_table('coworkers',
    sa.Column('user_from', sa.String(), nullable=False),
    sa.Column('user_to', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_from'], ['users.login'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_to'], ['users.login'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('user_from', 'user_to')
    )
    op.create_table('files',
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('user_from', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.Column('delete_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_from'], ['users.login'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('file_id')
    )
    op.create_table('file_users',
    sa.Column('file_user_id', sa.Integer(), nullable=False),
    sa.Column('user_to', sa.String(), nullable=True),
    sa.Column('secret_key', sa.String(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['files.file_id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_to'], ['users.login'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('file_user_id'),
    sa.UniqueConstraint('user_to', 'file_id', name='unique_fileid_for_user', postgresql_nulls_not_distinct=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_users')
    op.drop_table('files')
    op.drop_table('coworkers')
    op.drop_table('users')
    # ### end Alembic commands ###