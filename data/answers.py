"""Модель ответов"""
import datetime
import sqlalchemy

from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Answer(SqlAlchemyBase, SerializerMixin):
    """
    Модель ответов пользователей
    
    Содержит следующие поля:
      - id
      - answer
      - answered_date
      - user_id
      - user (relationship)
      - question_id
      - question (relationship)
    """
    __tablename__ = "answers"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    answer = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    answered_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
    )
    user = orm.relationship("User", back_populates="answers")

    question_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("questions.id", ondelete="CASCADE"),
    )
    question = orm.relationship("Question", back_populates="answers")
