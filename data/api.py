"""Функции API созданные с помощью Blueprint"""
from flask import Blueprint, jsonify
from data import db_session
from data.questions import Question
from data.likes import Like
from data.comments import Comment
from data.users import User

blueprint = Blueprint("api", __name__, template_folder="templates")


def __get_user_dict(user):
    return user.to_dict(
        only=(
            "id",
            "name",
            "email",
            "created_date",
            "admin",
        )
    )


@blueprint.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Возвращает json объект со всеми вопросами, внесёнными в базу данных

    Формат ответа:
    {
        'questions': [
            {
                'id': ...,              (int)
                'text': ...,            (str)
                'choice_1': ...,        (str)
                'choice_2': ...,        (str)
                'created_date': ...     (datetime)
            }, ...
        ]
    }

    В случае отсутствия вопросов возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    questions = db_sess.query(Question).all()

    if not questions:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "questions": [
                question.to_dict(
                    only=("id", "text", "choice_1", "choice_2", "created_date")
                )
                for question in questions
            ]
        }
    )


@blueprint.route("/api/users", methods=["GET"])
def get_users():
    """
    Возвращает json объект со всеми пользователями, зарегистрированными в системе

    Формат ответа:
    {
        'users': [
            {
                'id': ...,                  (int)
                'name': ...,                (str)
                'email': ...,               (str)
                'created_date': ...,        (datetime)
                'admin': ...                (int)
            }, ...
        ]
    }

    В случае отсутствия пользователей возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()

    if not users:
        return jsonify({"error": "Not found"})

    return jsonify({"users": [__get_user_dict(user) for user in users]})


@blueprint.route("/api/question/<int:id>", methods=["GET"])
def get_question(id):
    """
    Возвращает json, содержащий информацию о конкретном вопросе

    Обазательный агрумент: id вопроса

    Формат ответа:
    {
        'question': [
            {
                'id': ...,              (int)
                'text': ...,            (str)
                'choice_1': ...,        (str)
                'choice_2': ...,        (str)
                'created_date': ...     (datetime)
            }
        ]
    }

    В случае отсутствия вопросов возвращает ответ: {'error': 'Not found'}
    """
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
                "created_date": question.created_date,
            }
        }
    )


@blueprint.route("/api/user/<int:id>", methods=["GET"])
def get_user(id):
    """
    Возвращает json, содержащий информацию о конкретном пользователе

    Обазательный агрумент: id пользователя

    Формат ответа:
    {
        'user': {
            'id': ...,                  (int)
            'name': ...,                (str)
            'email': ...,               (str)
            'created_date': ...,        (datetime)
            'admin': ...                (int)
        }
    }

    В случае отсутствия пользователя возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    if not user:
        return jsonify({"error": "Not found"})

    return jsonify({"user": __get_user_dict(user)})


@blueprint.route("/api/user/<int:id>/answers", methods=["GET"])
def get_user_questions(id):
    """
    Возвращает json объект со всеми ответами, которые оставил пользователь

    Обазательный агрумент: id пользователя

    Формат ответа:
    {
        'answers': [
            {
                'id': ...,              (int)
                'text': ...,            (str)
                'choice_1': ...,        (str)
                'choice_2': ...,        (str)
                'created_date': ...     (datetime)
            }, ...
        ],
        'user': {
            'id': ...,                  (int)
            'name': ...,                (str)
            'email': ...,               (str)
            'created_date': ...,        (datetime)
            'admin': ...                (int)
        }
    }

    В случае отсутствия ответов возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    if not user:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "answers": [
                question.to_dict(
                    only=(
                        "id",
                        "answer",
                        "answered_date",
                        "user_id",
                        "question_id",
                    )
                )
                for question in user.answers
            ],
            "user": __get_user_dict(user),
        }
    )


@blueprint.route("/api/user/<int:id>/comments", methods=["GET"])
def get_user_comments(id):
    """
    Возвращает json объект со всеми комментариями, которые оставил конкретный пользователь

    Обазательный агрумент: id пользователя

    Формат ответа:
    {
        'comments': [
            {
                'id': ...,              (int)
                'text': ...,            (str)
                'user_id': ...,         (int)
                'question_id': ...,     (int)
                'created_date': ...,    (datetime)
                'likes_count': ...      (int)
            }, ...
        ],
        'user': {
            'id': ...,                  (int)
            'name': ...,                (str)
            'email': ...,               (str)
            'created_date': ...,        (datetime)
            'admin': ...                (int)
        }
    }

    В случае отсутствия комментариев возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).filter(Comment.user_id == id)
    user = db_sess.query(User).get(id)

    if not comments:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "comments": [
                comment.to_dict(
                    only=(
                        "id",
                        "text",
                        "user_id",
                        "question_id",
                        "created_date",
                        "likes_count",
                    )
                )
                for comment in comments
            ],
            "user": __get_user_dict(user),
        }
    )


@blueprint.route("/api/user/<int:id>/likes", methods=["GET"])
def get_user_likes(id):
    """
    Возвращает json объект со всеми лайками, которые оставил конкретный пользователь

    Обазательный агрумент: id пользователя

    Формат ответа:
    {
        'likes': [
            {
                'id': ...,              (int)
                'user_id': ...,         (int)
                'comment_id': ...       (int)
            }, ...
        ],
        'user': {
            'id': ...,                  (int)
            'name': ...,                (str)
            'email': ...,               (str)
            'created_date': ...,        (datetime)
            'admin': ...                (int)
        }
    }

    В случае отсутствия лайков возвращает ответ: {'error': 'Not found'}
    """
    db_sess = db_session.create_session()
    comments = db_sess.query(Like).filter(Comment.user_id == id)
    user = db_sess.query(User).get(id)

    if not comments:
        return jsonify({"error": "Not found"})

    return jsonify(
        {
            "likes": [
                comment.to_dict(only=("id", "comment_id", "user_id"))
                for comment in comments
            ],
            "user": __get_user_dict(user),
        }
    )
