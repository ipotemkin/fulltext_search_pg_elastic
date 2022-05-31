import sqlalchemy as sa
from sqlalchemy import func

metadata = sa.MetaData()

posts = sa.Table(
    'post',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('rubrics', sa.String, nullable=True),
    sa.Column('text', sa.Text, nullable=True),
    sa.Column('created_date', sa.DateTime, server_default=func.now()),
    sa.Column('updated', sa.DateTime, onupdate=func.now()),
)
