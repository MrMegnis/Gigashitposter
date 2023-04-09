import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase


class Tags(SqlAlchemyBase, UserMixin):
    __tablename__ = "tags"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_deviant_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
