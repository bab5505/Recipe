# 1234567890_create_users_table.py

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=False)
    )


def downgrade():
    op.drop_table('users')
