from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, URL,
    Regexp, ValidationError
)

from yacut.models import URLMap
from yacut.constants import (
    INVALID_SHORT, INVALID_URL,
    CUSTOM_ID_DESCRIPTION, DATA_REQUIRED,
    MAX_LENGTH_USERS_SHORT, MAX_URL_LENGTH,
    ORIGINAL_DESCRIPTION, SHORT_EXISTS,
    SUBMIT_BUTTON_TEXT, SHORT_REGULAR
)


class MainForm(FlaskForm):
    """Форма для генерации ссылки."""
    original_link = URLField(
        ORIGINAL_DESCRIPTION,
        validators=[
            DataRequired(message=DATA_REQUIRED),
            Length(max=MAX_URL_LENGTH),
            URL(message=INVALID_URL)
        ])
    custom_id = StringField(
        CUSTOM_ID_DESCRIPTION,
        validators=[
            Length(max=MAX_LENGTH_USERS_SHORT),
            Optional(),
            Regexp(SHORT_REGULAR, message=INVALID_SHORT)
        ])
    submit = SubmitField(SUBMIT_BUTTON_TEXT)

    def validate_custom_id(self, field):
        """Проверка существования короткой ссылки."""
        if field.data:
            if URLMap.get_short_link_exists(short=field.data):
                raise ValidationError(SHORT_EXISTS)
