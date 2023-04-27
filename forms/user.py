from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired

# Форма регестрации
class RegisterForm(FlaskForm):
    """
    -name Имя пользователя
    -photo Фото профиля пользователя
    -email Эмайл пользователя
    -password Пароль пользователя
    -password_again Повторение пороля пользователя
    -submit Кнопка подтверждения
    """
    name = StringField('Имя пользователя', validators=[DataRequired()])
    photo = FileField('Фото профиля', validators=[FileAllowed(('jpg', 'jpeg', 'png'), 'Допускаются только картинки!'), FileRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Форма входа
class LoginForm(FlaskForm):
    """
    -email Эмайл пользователя
    -password Пароль пользователя
    -remember_me Запомнить пользователя да или нет
    -submit Кнопка подтверждения
    """
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
