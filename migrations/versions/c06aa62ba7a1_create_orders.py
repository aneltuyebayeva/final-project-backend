"""create-orders

Revision ID: c06aa62ba7a1
Revises: ae6230cbe2c8
Create Date: 2021-05-21 15:52:24.266636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c06aa62ba7a1'
down_revision = 'ae6230cbe2c8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('address', sa.String),
        sa.Column('credit_card', sa.String)
    )


def downgrade():
    op.drop_table('orders')
