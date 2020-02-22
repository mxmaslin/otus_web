from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo


from .models import User, Tag


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста введите другое имя пользователя')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TagField(StringField):
    def _value(self):
        if self.data:
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        new_tags = [Tag(name=name) for name in new_names]
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    body = StringField('Текст поста', validators=[DataRequired()])
    tags = TagField('Теги', description='Разделитель - запятая')
    submit = SubmitField('Опубликовать')
