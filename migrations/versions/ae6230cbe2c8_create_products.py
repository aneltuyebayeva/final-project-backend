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
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('image', sa.String),
        sa.Column('price', sa.String),
    )


def downgrade():
    op.drop_table('products')
