# Форма вопросов
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    """
    -text Текст вопроса
    -choice_1 Первый вариант выбора
    -choice_2 Второй вариант выбора
    -submit Кнопка подтверждения
    """
    text = StringField('Текст', validators=[DataRequired()])
    choice_1 = StringField('Вариант 1', validators=[DataRequired()])
    choice_2 = StringField('Вариант 2', validators=[DataRequired()])
    submit = SubmitField('Добавить')
