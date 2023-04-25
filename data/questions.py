import datetime
import sqlalchemy

from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "questions"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    choice_1 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    choice_2 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )

    comments = orm.relationship(
        "Comment", back_populates="question", cascade="all, delete"
    )
    answers = orm.relationship(
        "Answer", back_populates="question", cascade="all, delete"
    )
