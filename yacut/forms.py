from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL

from settings import MAX_LENGTH_USERS


class MainForm(FlaskForm):
    """Форма для генерации ссылки."""
    original_link = URLField(
        'Вставьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128),
            URL(message='Введите корректный URL')
        ])
    custom_id = StringField(
        'Желаемая короткая ссылка',
        validators=[Length(0, MAX_LENGTH_USERS)])
    submit = SubmitField('Создать')
