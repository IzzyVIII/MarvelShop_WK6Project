"""empty message

Revision ID: 530e66487b48
Revises: 370b9207dd79
Create Date: 2023-11-19 21:46:10.779160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '530e66487b48'
down_revision = '370b9207dd79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('img')

    # ### end Alembic commands ###
