"""create-products

Revision ID: 35c54188d07e
Revises: 1a1555ed307d
Create Date: 2021-05-21 16:39:43.950182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c54188d07e'
down_revision = '1a1555ed307d'
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
