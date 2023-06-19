"""Add user table

Revision ID: 9fbc94d8bb5d
Revises: <previous_revision_id>  # Replace with the actual previous revision ID
Create Date: 2023-05-29  # Replace with the appropriate create date

"""

from alembic import op
import sqlalchemy as sa


# Replace '<previous_revision_id>' with the actual previous revision ID
revision = '9fbc94d8bb5d'
down_revision = '<previous_revision_id>'


def upgrade():
    # Drop the foreign key constraint on the 'recipes' table
    op.drop_constraint('recipes_user_id_fkey', 'recipes', type_='foreignkey')

    # Drop the 'users' table
    op.drop_table('users')


def downgrade():
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Add the foreign key constraint back to the 'recipes' table
    op.create_foreign_key(
        'recipes_user_id_fkey', 'recipes', 'users', ['user_id'], ['id']
    )
