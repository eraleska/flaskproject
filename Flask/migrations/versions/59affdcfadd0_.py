"""empty message

Revision ID: 59affdcfadd0
Revises: 41a91e095487
Create Date: 2023-09-22 14:10:35.909910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59affdcfadd0'
down_revision = '41a91e095487'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('age')

    # ### end Alembic commands ###