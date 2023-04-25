import datetime
import sqlalchemy

from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "comments"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    text = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(
        sqlalchemy.String,
        default=f"{datetime.datetime.now().strftime('%H:%M - %d.%m.%Y')}",
    )

    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
    )
    user = orm.relationship("User", back_populates="comments")

    question_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("questions.id", ondelete="CASCADE"),
        index=True,
    )
    question = orm.relationship("Question", back_populates="comments")

    likes = orm.relationship(
        "Like", back_populates="comment"
    )
    likes_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def update_likes_count(self):
        self.likes_count = len(self.likes)
