from flask import Blueprint, jsonify
from data import db_session
from data.questions import Question
from data.comments import Comment

blueprint = Blueprint("api", __name__, template_folder="templates")


@blueprint.route("/api/questions", methods=["GET"])
def get_questions():
    db_sess = db_session.create_session()
    questions = db_sess.query(Question).all()

    if not questions:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "questions": [
                question.to_dict(only=("text", "choice_1", "choice_2", "created_date"))
                for question in questions
            ]
        }
    )


@blueprint.route("/api/question/<int:id>", methods=["GET"])
def get_question(id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(id)

    if not question:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "question": {
                "id": question.id,
                "text": question.text,
                "choice_1": question.choice_1,
                "choice_2": question.choice_2,
                "created_date": question.created_date
            }
        }
    )

@blueprint.route("/api/user/<int:id>/questions", methods=["GET"])
def get_user_questions(id):
    db_sess = db_session.create_session()
    questions = db_sess.query(Question).filter(Question.user_id == id)

    if not questions:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "questions": [
                question.to_dict(only=("id", "text", "choice_1", "choice_2", "created_date"))
                for question in questions
            ]
        }
    )

@blueprint.route("/api/user/<int:id>/comments", methods=["GET"])
def get_user_questions(id):
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).filter(Comment.user_id == id)

    if not comments:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "comments": [
                comment.to_dict(only=("id", "text", "user_id", "question_id", "created_date", "likes_count"))
                for comment in comments
            ]
        }
    )
