# Форма вопросов
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    text = StringField('Текст', validators=[DataRequired()])
    choice_1 = StringField('Вариант 1', validators=[DataRequired()])
    choice_2 = StringField('Вариант 2', validators=[DataRequired()])
    submit = SubmitField('Добавить')
