# Импорты
from flask import (
    Flask,
    render_template,
    redirect,
    abort,
    request,
    url_for,
    jsonify,
)
from config import SECRET_KEY, ADMIN_KEY
from data import api, db_session
from data.users import User
from data.answers import Answer
from data.questions import Question
from data.comments import Comment
from data.likes import Like
from forms.user import RegisterForm, LoginForm
from forms.questions import QuestionForm
from forms.comment import CommentForm
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy.sql import func
from PIL import Image
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


# Функция для сохранения изображения профиля пользоввателя
def save_image(photo, file_path):
    img = Image.open(photo)

    width, height = img.size
    size = (min(width, height), min(width, height))

    img = img.crop((0, 0, size[0], size[1]))
    img.thumbnail((256, 256), Image.ANTIALIAS)

    img.save(file_path)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Дбавление вопросов
@app.route("/add/question", methods=["GET", "POST"])
@login_required
def add_question():
    """
    Подключаем форму и интерфейс и добавляем вопрос
    """
    if not current_user.admin:
        abort(401)

    form = QuestionForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        question = Question()

        question.text = form.text.data
        question.choice_1 = form.choice_1.data
        question.choice_2 = form.choice_2.data

        db_sess.add(question)
        db_sess.commit()

        return redirect("/admin")

    return render_template(
        "add-question.html", title="Создание вопроса", form=form
    )


# Изменение вопросов
@app.route("/edit/question/<int:id>", methods=["GET", "POST"])
@login_required
def edit_question(id):
    """
    подключаем форму и интерфейс
    Args:
        id (_type_): Если вопрос существует в базе данных
    Returns:
        _type_: Изменение вопроса
    """
    if not current_user.admin:
        abort(401)

    form = QuestionForm()
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(id)

    if not question:
        abort(404)

    if request.method == "GET":
        form.text.data = question.text
        form.choice_1.data = question.choice_1
        form.choice_2.data = question.choice_2

    if form.validate_on_submit():
        question.text = form.text.data
        question.choice_1 = form.choice_1.data
        question.choice_2 = form.choice_2.data

        db_sess.commit()

        return redirect("/admin")

    return render_template(
        "add-question.html", title="Измение вопроса", form=form
    )


# Удаление вопросов
@app.route("/delete/question/<int:id>")
@login_required
def delete_question(id: int):
    """
    Подключение к базе данных
    Args:
        id (int): Если вопрос существует в бузе данных 
    Returns:
        _type_: Удаление выбранного вопроса
    """
    if not current_user.admin:
        abort(401)

    db_sess = db_session.create_session()

    question = db_sess.query(Question).get(id)

    db_sess.delete(question)
    db_sess.commit()

    return "Ok"


# Обновление количества лайков
@app.route("/add/like/comment/<int:id>", methods=["GET"])
@login_required
def like(id):
    """
    Получене данных
    Args:
        id (_type_): Проверка id лайка и комментария
    Returns:
        _type_: Добавление или убывание лайка
    """
    db_sess = db_session.create_session()

    comment = db_sess.query(Comment).get(id)
    like = (
        db_sess.query(Like)
        .filter(Like.comment_id == id, Like.user_id == current_user.id)
        .first()
    )

    if like:
        db_sess.delete(like)
    else:
        like = Like(comment_id=comment.id, user_id=current_user.id)
        db_sess.add(like)

    comment.update_likes_count()
    db_sess.commit()

    return jsonify(comment.likes_count)


# Удаление комментариев
@app.route("/delete/comment/<int:id>")
@login_required
def delete_comment(id: int):
    """
    Получение данных
    Args:
        id (int): Если айди комментария верный и комментарий принадлежит пользователю
    """
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(id)

    if comment.user_id != current_user.id:
        abort(401)

    db_sess.delete(comment)
    db_sess.commit()

    return jsonify(db_sess.query(Comment).count())


# Личный кабинет
@app.route("/lk")
@login_required
def lk():
    """
    Открытие личного кабинета
    Returns:
        _type_: Личный кабинет
    """
    db_sess = db_session.create_session()
    answers = (
        db_sess.query(Answer).filter(Answer.user_id == current_user.id).all()
    )

    return render_template(
        "lk.html",
        title="Аккаунт",
        answers=answers,
        user_avatar=url_for(
            "static", filename=f"avatars/{current_user.id}.png"
        ),
    )


# Раздел администрирования
@app.route("/admin")
@login_required
def admin_panel():
    """
    Открытие панели администрирования
    """
    if not current_user.admin:
        abort(401)

    db_sess = db_session.create_session()
    questions = db_sess.query(Question).all()

    return render_template(
        "admin.html",
        title="Администрирование",
        questions=questions,
    )


# Переадресация на главную страницу с вопросами
@app.route("/")
def index():
    """
    Главная страница с выбором
    Returns:
        _type_: Вопрос
    """
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        answered_questions = (
            db_sess.query(Answer.question_id)
            .filter_by(user_id=current_user.id)
            .all()
        )

        answered_question_ids = [q[0] for q in answered_questions]
        question = (
            db_sess.query(Question)
            .filter(Question.id.notin_(answered_question_ids))
            .order_by(func.random())
            .first()
        )
    else:
        question = db_sess.query(Question).order_by(func.random()).first()

    return render_template(
        "index.html",
        title=f"Вопрос #{question.id}" if question else "Вопросы закончились",
        question=question,
    )


# Открыть определённый вопрос по id
@app.route("/<int:id>")
def get_question(id):
    """
    Вывод определённого вопроса
    Args:
        id (_type_): Если айди есть в базе

    Returns:
        _type_: Вопрос
    """
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(id)

    return render_template(
        "index.html", title=f"Вопрос #{id}", question=question
    )


# Страничка с результатом ответов
@app.route("/<int:id>/<int:answer>/res", methods=["GET", "POST"])
def result(id, answer):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).get(id)

    if not question or answer not in (1, 2):
        abort(404)

    if (
        current_user.is_authenticated
        and not db_sess.query(Answer)
        .filter(Answer.user_id == current_user.id, Answer.question_id == id)
        .first()
    ):
        new_answer = Answer(
            answer=answer, question_id=question.id, user_id=current_user.id
        )

        db_sess.add(new_answer)
        db_sess.commit()

    comments = (
        db_sess.query(Comment).filter(Comment.question_id == question.id).all()
    )

    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            abort(401)

        db_sess = db_session.create_session()

        new_comment = Comment(
            text=form.text.data,
            user_id=current_user.id,
            question_id=question.id,
        )

        db_sess.add(new_comment)
        db_sess.commit()

        return redirect(request.referrer)

    answer_1 = (
        db_sess.query(Answer).filter_by(question_id=id, answer=1).count()
    )
    answer_2 = (
        db_sess.query(Answer).filter_by(question_id=id, answer=2).count()
    )

    try:
        per_1 = answer_1 * 100 // (answer_1 + answer_2)
    except ZeroDivisionError:
        per_1 = 0

    per_2 = 100 - per_1

    return render_template(
        "result.html",
        title=f"Ответы на вопрос #{id}",
        question=question,
        answer=answer,
        answer_1=answer_1,
        answer_2=answer_2,
        comments=comments,
        per_1=per_1,
        per_2=per_2,
        form=form,
    )


# Регистрация
@app.route("/register", methods=["GET", "POST"])
def reqister():
    """
    Регестрационное поле с проверкой на то что все данные введены верно
    """
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )

        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)

        if request.args.get("admin_key") == ADMIN_KEY:
            user.admin = True

        db_sess.add(user)
        db_sess.commit()

        file_path = os.path.join("static", "avatars", f"{user.id}.png")
        save_image(form.photo.data, file_path)

        login_user(user, remember=True)
        return redirect("/")

    return render_template("register.html", title="Регистрация", form=form)

# Информация о сайте
@app.route('/info')
def info():
    return render_template('info.html')


# Вход в аккаунт
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Вход в аккаунт с проверкай на правильность введённых данных
    """
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template(
            "login.html",
            title="Авторизация",
            message="Неправильный логин или пароль",
            form=form,
        )

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect("/")


@app.errorhandler(401)
def bad_request(_):
    return redirect("/login")


# Сообщение об ошибке
@app.errorhandler(404)
def bad_request(_):
    return render_template("404.html", title="Страница не найдена")


def main() -> None:
    if not os.path.exists("db"):
        os.makedirs("db")

    db_session.global_init("db/app.db")
    app.register_blueprint(api.blueprint)
    app.run()


if __name__ == "__main__":
    main()
