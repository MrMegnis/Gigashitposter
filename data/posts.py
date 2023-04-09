import datetime
import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm


class Posts(SqlAlchemyBase, UserMixin):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    user = orm.relationship('Users')
