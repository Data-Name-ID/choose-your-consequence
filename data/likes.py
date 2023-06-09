"""Модель лайков"""
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Like(SqlAlchemyBase, SerializerMixin):
    """
    Модель лайков пользователей

    Содержит следующие поля:
      - id
      - comment_id
      - comment (relationship)
      - user_id
      - user (relationship)
    """

    __tablename__ = "likes"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # поле оставлено для совместимости

    comment_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("comments.id"),
        index=True,
    )
    comment = orm.relationship("Comment", back_populates="likes")

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
    )
    user = orm.relationship("User", back_populates="likes")
