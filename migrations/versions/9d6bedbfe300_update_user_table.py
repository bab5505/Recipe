"""Update user table

Revision ID: 9d6bedbfe300
Revises: d006e53d1a50
Create Date: 2023-06-23 15:23:01.727487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d6bedbfe300'
down_revision = 'd006e53d1a50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('recipes')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recipe_user_id', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('image_url',
               existing_type=sa.TEXT(),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.drop_constraint('uq_user_id', type_='unique')
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    op.drop_table('users')
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('uq_user_id', ['id'])
        batch_op.alter_column('image_url',
               existing_type=sa.String(length=200),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

#     with op.batch_alter_table('recipe', schema=None) as batch_op:
#         batch_op.drop_constraint(None, type_='foreignkey')
#         batch_op.create_foreign_key('fk_recipe_user_id', 'user', ['user_id'], ['id'])

    op.create_table('recipes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('instructions', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('ingredients', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('prep_time', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('servings', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='recipes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='recipes_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    # ### end Alembic commands ###