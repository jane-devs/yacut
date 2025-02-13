from datetime import datetime
import re

from flask import request

from yacut import db
from yacut.error_handlers import InvalidAPIUsage
from settings import (
    API_INVALID_SHORT, MAX_LENGTH_USERS, MAX_URL_LENGTH,
    SHORT_EXISTS, SHORT_REGULAR, check_short_link_exists,
    get_unique_short_id

)


class URLMap(db.Model):
    """Модель для хранения информации о сокращенных URL."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_USERS), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_dict(self):
        """Метод превращения JSON в словарь."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    @staticmethod
    def get_or_create(original, short=None):
        """Проверяет существование пользовательской короткой ссылки.
        Если не существует, то создает новую."""
        if short not in [None, ""]:
            if check_short_link_exists(model=URLMap, short=short):
                raise InvalidAPIUsage(SHORT_EXISTS)
            if not re.match(SHORT_REGULAR, short) or (
                len(short) > MAX_LENGTH_USERS
            ):
                raise InvalidAPIUsage(API_INVALID_SHORT)
        else:
            short = get_unique_short_id()
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return {
            'url': urlmap.original,
            'short_link': request.host_url + urlmap.short
        }
