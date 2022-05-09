"""added relationship crypto to watchlist

Revision ID: 0a57ea1774a5
Revises: 83b4e0d49f9a
Create Date: 2022-05-09 12:07:03.977862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a57ea1774a5'
down_revision = '83b4e0d49f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_crypto_id', 'crypto', ['crypto_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
