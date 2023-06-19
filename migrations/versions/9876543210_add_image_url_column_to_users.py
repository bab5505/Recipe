"""Add user table

Revision ID: 9876543210
Revises: 1234567890
Create Date: 2023-05-29 12:34:56.789012

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9876543210'
down_revision = '1234567890'
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'image_url' column to the 'users' table
      op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
        

def downgrade():
    # Drop the 'image_url' column from the 'users' table
    op.drop_column('users', 'image_url')
