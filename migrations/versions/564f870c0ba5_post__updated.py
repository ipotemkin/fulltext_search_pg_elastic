"""post__updated

Revision ID: 564f870c0ba5
Revises: c5d6dd382c30
Create Date: 2022-05-28 23:09:02.749066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '564f870c0ba5'
down_revision = 'c5d6dd382c30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('updated', sa.DateTime(), onupdate=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'updated')
    # ### end Alembic commands ###
