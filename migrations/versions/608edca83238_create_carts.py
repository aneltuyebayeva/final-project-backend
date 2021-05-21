"""create-carts

Revision ID: 608edca83238
Revises: 02cefbf622e4
Create Date: 2021-05-21 15:52:04.565811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '608edca83238'
down_revision = '02cefbf622e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
    )


def downgrade():
    op.drop_table('carts')
