import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Webhook(SqlAlchemyBase, UserMixin):
    __tablename__ = "webhooks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    ds_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    ds_url = sqlalchemy.Column(sqlalchemy.String)
    guild_id = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('Users')
