"""create-products

Revision ID: ae6230cbe2c8
Revises: 608edca83238
Create Date: 2021-05-21 15:52:15.259144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae6230cbe2c8'
down_revision = '608edca83238'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
    )


def downgrade():
    op.drop_table('products')
