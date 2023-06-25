"""empty message

Revision ID: d006e53d1a50
Revises: 39a4621bc82a
Create Date: 2023-06-21 12:16:06.007953

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd006e53d1a50'
down_revision = '39a4621bc82a'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the foreign key constraint in the 'recipes' table
    op.drop_constraint('recipes_user_id_fkey', 'recipes', type_='foreignkey')

    # Drop the primary key constraint in the 'users' table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_pkey', type_='primary')

    # Drop the old tables
    op.drop_table('users')
    op.drop_table('recipes')

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),  # Assuming 'image_url' is an optional field
        sa.UniqueConstraint('email', name='users_email_key'),
        sa.UniqueConstraint('username', name='users_username_key')
    )

    op.create_table('recipes',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=80), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('ingredients', sa.Text(), nullable=False),
        sa.Column('prep_time', sa.String(length=20), nullable=False),
        sa.Column('servings', sa.String(length=20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='recipes_user_id_fkey')
    )


def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint('recipes_user_id_fkey', 'recipes', type_='foreignkey')

    # Drop the new tables
    op.drop_table('users')
    op.drop_table('recipes')

    # Create the old tables
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),  # Assuming 'image_url' is an optional field
        sa.UniqueConstraint('email', name='users_email_key'),
        sa.UniqueConstraint('username', name='users_username_key')
    )

    op.create_table('recipes',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=80), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('ingredients', sa.Text(), nullable=False),
        sa.Column('prep_time', sa.String(length=20), nullable=False),
        sa.Column('servings', sa.String(length=20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='recipes_user_id_fkey')
    )
