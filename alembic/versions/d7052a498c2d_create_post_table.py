"""create post table

Revision ID: d7052a498c2d
Revises: 
Create Date: 2023-07-28 15:58:25.804816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7052a498c2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('post', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table('post')
    pass
