from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '39a4621bc82a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
      # Drop the old foreign key constraint
    op.drop_constraint('recipes_user_id_fkey', 'recipes', type_='foreignkey')
    op.drop_table('users', cascade=True)
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('username', sa.Text(), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('password', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_foreign_key(
        'recipes_user_id_fkey',
        'recipes',
        'user',
        ['user_id'],
        ['id']
    )

def downgrade():
    op.create_table('users', ...)
    op.create_foreign_key('recipes_user_id_fkey', 'recipes', 'users', ['user_id'], ['id'])
    op.drop_table('user')

    # ### end Alembic commands ###
