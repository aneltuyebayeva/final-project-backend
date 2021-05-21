"""create-product_orders

Revision ID: 1a1555ed307d
Revises: c06aa62ba7a1
Create Date: 2021-05-21 15:52:41.455588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a1555ed307d'
down_revision = 'c06aa62ba7a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'product_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer),
        sa.Column('order_id', sa.Integer),
    )


def downgrade():
    op.drop_table('product_orders')
