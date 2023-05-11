"""empty message

Revision ID: 6db9a6052609
Revises: fc2c0fad5f59
Create Date: 2023-05-11 20:57:00.663983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6db9a6052609'
down_revision = 'fc2c0fad5f59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('img', sa.String(), nullable=True))
    op.drop_column('movies', 'total_audience')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('total_audience', sa.VARCHAR(), nullable=True))
    op.drop_column('movies', 'img')
    # ### end Alembic commands ###