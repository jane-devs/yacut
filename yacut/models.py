from datetime import datetime
from random import choice
import re
from urllib.parse import urljoin

from flask import request
from wtforms import ValidationError

from yacut import db
from settings import (
    API_INVALID_SHORT, MAX_LENGTH_USERS, MAX_URL_LENGTH,
    MAX_LENGTH_GENERATE, SHORT_EXISTS,
    SHORT_REGULAR, SYMBOLS_STR, URL_REQUIRED
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
    def create(original, short=None, form_validated=False):
        """Проверяет существование пользовательской короткой ссылки.
        Если не существует, то создает новую."""
        if not short:
            short = URLMap.get_unique_short_id()
        if not form_validated:
            if not re.match(SHORT_REGULAR, short) or (
                len(short) > MAX_LENGTH_USERS
            ):
                raise Exception(API_INVALID_SHORT)
            if URLMap.check_short_link_exists(short=short):
                raise Exception(SHORT_EXISTS)
        if original in [None, '']:
            raise Exception(URL_REQUIRED)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def check_short_link_exists(short):
        """Метод модели для проверки существования короткой ссылки."""
        return URLMap.query.filter_by(short=short).first()

    def validate_short_link(self, short):
        """Метод модели для валидации короткой ссылки."""
        if short and self.check_short_link_exists(short):
            raise ValidationError(SHORT_EXISTS)

    @staticmethod
    def get_unique_short_id():
        """Метод модели для получения уникальной короткой ссылки."""
        return ''.join(choice(SYMBOLS_STR) for _ in range(MAX_LENGTH_GENERATE))

    @staticmethod
    def get_full_url(short):
        """Метод модели для получения полного URL из короткой ссылки."""
        return urljoin(request.host_url, short)
