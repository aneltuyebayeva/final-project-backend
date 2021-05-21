"""create-users

Revision ID: 02cefbf622e4
Revises: 
Create Date: 2021-05-21 15:34:16.255791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02cefbf622e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String),
    )


def downgrade():
    op.drop_table('users')
