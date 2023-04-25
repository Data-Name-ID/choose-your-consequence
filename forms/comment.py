from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    text = StringField('Текст', validators=[DataRequired()])
    submit = SubmitField('Комментировать')
