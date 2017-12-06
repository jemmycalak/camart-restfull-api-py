"""empty message

Revision ID: 1cd2fccd26fe
Revises: 3bfcd49c1100
Create Date: 2017-11-27 23:13:17.357000

"""

# revision identifiers, used by Alembic.
revision = '1cd2fccd26fe'
down_revision = '3bfcd49c1100'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_address', sa.Column('isDelete', sa.TIMESTAMP(), nullable=True))
    op.add_column('t_bank', sa.Column('isDelete', sa.TIMESTAMP(), nullable=True))
    op.add_column('t_cart', sa.Column('isDelete', sa.TIMESTAMP(), nullable=True))
    op.add_column('t_order', sa.Column('isDelete', sa.TIMESTAMP(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_order', 'isDelete')
    op.drop_column('t_cart', 'isDelete')
    op.drop_column('t_bank', 'isDelete')
    op.drop_column('t_address', 'isDelete')
    ### end Alembic commands ###