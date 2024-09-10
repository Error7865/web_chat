"""Adding new column online to user table

Revision ID: df37f1796e65
Revises: f7f6c4906cd4
Create Date: 2024-06-28 18:59:04.548432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df37f1796e65'
down_revision = 'f7f6c4906cd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Online', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('Online')

    # ### end Alembic commands ###