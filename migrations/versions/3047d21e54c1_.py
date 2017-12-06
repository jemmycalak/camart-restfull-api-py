"""empty message

Revision ID: 3047d21e54c1
Revises: 1cd2fccd26fe
Create Date: 2017-11-27 23:18:06.232000

"""

# revision identifiers, used by Alembic.
revision = '3047d21e54c1'
down_revision = '1cd2fccd26fe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_bukti_pembayaran',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_order', sa.Integer(), nullable=True),
    sa.Column('img_url', sa.TEXT(), nullable=False),
    sa.Column('createDate', sa.TIMESTAMP(), nullable=True),
    sa.Column('updateDate', sa.TIMESTAMP(), nullable=True),
    sa.Column('isDelete', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['id_order'], ['t_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_bukti_pembayaran')
    ### end Alembic commands ###
