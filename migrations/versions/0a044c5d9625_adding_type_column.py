"""Adding type column 

Revision ID: 0a044c5d9625
Revises: f431f4c07471
Create Date: 2024-07-15 18:27:55.797025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a044c5d9625'
down_revision = 'f431f4c07471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Type', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('daily', schema=None) as batch_op:
        batch_op.drop_column('Type')

    # ### end Alembic commands ###
