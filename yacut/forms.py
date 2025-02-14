from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from yacut.models import URLMap
from settings import (
    API_INVALID_SHORT, API_INVALID_URL, CUSTOM_ID_DESCRIPTION,
    DATA_REQUIRED, MAX_LENGTH_USERS, MAX_URL_LENGTH,
    ORIGINAL_DESCRIPTION, SHORT_REGULAR, SUBMIT_BUTTON_TEXT
)


class MainForm(FlaskForm):
    """Форма для генерации ссылки."""
    original_link = URLField(
        ORIGINAL_DESCRIPTION,
        validators=[
            DataRequired(message=DATA_REQUIRED),
            Length(max=MAX_URL_LENGTH),
            URL(message=API_INVALID_URL)
        ])
    custom_id = StringField(
        CUSTOM_ID_DESCRIPTION,
        validators=[
            Length(max=MAX_LENGTH_USERS),
            Optional(),
            Regexp(SHORT_REGULAR, message=API_INVALID_SHORT)
        ])
    submit = SubmitField(SUBMIT_BUTTON_TEXT)

    def validate_custom_id(self, field):
        """Проверка существования короткой ссылки."""
        URLMap().validate_short_link(field.data)
