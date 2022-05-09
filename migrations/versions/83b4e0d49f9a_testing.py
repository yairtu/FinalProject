"""testing

Revision ID: 83b4e0d49f9a
Revises: 
Create Date: 2022-05-08 21:13:47.735230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83b4e0d49f9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crypto',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.String(length=20), nullable=True),
    sa.Column('kucoin_name', sa.String(length=20), nullable=True),
    sa.Column('kucoin_price_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('usd', sa.Float(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('crypto_id', sa.Integer(), nullable=True),
    sa.Column('ticker', sa.String(length=10), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trade',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trade_time', sa.DateTime(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('current_price', sa.Float(), nullable=True),
    sa.Column('crypto_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('buy', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['crypto_id'], ['crypto.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('crypto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist')
    op.drop_table('trade')
    op.drop_table('portfolio')
    op.drop_table('user')
    op.drop_table('crypto')
    # ### end Alembic commands ###
