"""add image path column

Revision ID: dece519e6479
Revises: 000
Create Date: 2023-05-08 01:30:33.154836

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('avatars')
    op.drop_table('item_images')
    op.add_column('items', sa.Column('image_path', sa.String(length=256), nullable=True))
    op.add_column('users', sa.Column('avatar_path', sa.String(length=256), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'avatar_path')
    op.drop_column('items', 'image_path')
    op.create_table(
        'item_images',
        sa.Column('image_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True),
        sa.Column('is_first', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], name='item_images_item_id_fkey'),
        sa.PrimaryKeyConstraint('image_id', name='item_images_pkey'),
    )
    op.create_table(
        'avatars',
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='avatars_user_id_fkey'),
        sa.PrimaryKeyConstraint('user_id', name='avatars_pkey'),
    )
