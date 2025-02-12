"""Adding media column to Message

Revision ID: 6ab07a8a144f
Revises: 6ab6de2229a0
Create Date: 2024-08-01 17:24:06.660128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ab07a8a144f'
down_revision = '6ab6de2229a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Media', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('Media')

    # ### end Alembic commands ###
