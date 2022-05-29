import sqlalchemy as sa
from sqlalchemy import func

from src.dependencies import get_engine

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


# users = sa.Table(
#     'user',
#     metadata,
#     sa.Column('id', sa.BigInteger, primary_key=True),
#     sa.Column('login', sa.String, nullable=False),
#     sa.Column('name', sa.String, nullable=False)
# )
#
# post = sa.Table(
#     'post',
#     metadata,
#     sa.Column('id', sa.BigInteger, primary_key=True),  # TODO add comments on altering repo_id to id
#     sa.Column('user_id', sa.BigInteger, sa.ForeignKey('user.id'), nullable=False),  # TODO add cascade
#     sa.Column('repo_id', sa.BigInteger, nullable=True),  # TODO add comments on altering repo_id to id
#     sa.Column('date', sa.Date, nullable=False),
#     sa.Column('stargazers', sa.Integer, nullable=False),
#     sa.Column('forks', sa.Integer, nullable=False),
#     sa.Column('watchers', sa.Integer, nullable=False)
# )

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker


# def my_before_commit(session):
#     print("before commit!")
#
#
# Session = sessionmaker(bind=get_engine())
#
# event.listen(Session, "before_commit", my_before_commit)
#
#
# my_before_commit(Session)
