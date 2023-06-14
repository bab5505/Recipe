# 9876543210_add_image_url_column_to_users.py

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('image_url', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('users', 'image_url')
