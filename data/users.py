import datetime
import sqlalchemy

from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=False
    )
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    comments = orm.relationship(
        "Comment", back_populates="user", cascade="all, delete"
    )
    answers = orm.relationship(
        "Answer", back_populates="user", cascade="all, delete"
    )
    likes = orm.relationship(
        "Like", back_populates="user", cascade="all, delete"
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
