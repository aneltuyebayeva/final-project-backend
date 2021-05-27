"""create-add-quantity

Revision ID: 024b26b56c5e
Revises: 35c54188d07e
Create Date: 2021-05-27 14:36:41.927536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024b26b56c5e'
down_revision = '35c54188d07e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product_orders', 
    sa.Column('quantity', sa.Integer),
    )


def downgrade():
    op.drop_column('product_orders', 'quantity')
