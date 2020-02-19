from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo


from models import session, User


def unique_required(form, field):
    users = session.query(User).filter(User.name == field.data).all()
    if len(users) > 0:
        raise ValidationError('Пользователь с таким именем уже существует')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя', [DataRequired(), unique_required]
    )
    password = PasswordField('Пароль', [DataRequired(), EqualTo(
        'confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')
    submit = SubmitField('Зарегистироваться')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Помнить меня')
    submit = SubmitField('Войти')
