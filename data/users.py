import datetime
import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm


class Users(SqlAlchemyBase, UserMixin):
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tg_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    vk_access_token = sqlalchemy.Column(sqlalchemy.String)
    ds_id = sqlalchemy.Column(sqlalchemy.String)

    webhooks = orm.relationship("Webhook", back_populates='user')
    posts = orm.relationship("Posts", back_populates='user')