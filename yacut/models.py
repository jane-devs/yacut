from datetime import datetime
import random
import re

from flask import url_for

from yacut import db
from yacut.constants import (
    INVALID_SHORT, MAX_LENGTH_GENERATE_SHORT,
    GENERATE_FAIL, MAX_LENGTH_USERS_SHORT, MAX_URL_LENGTH,
    MAX_GENERATE_ATTEMPTS, SHORT_EXISTS,
    SHORT_REGULAR, SYMBOLS_STR, SHORT_URL_REDIRECT_NAME,
    URL_REQUIRED
)


class URLMap(db.Model):
    """Модель для хранения информации о сокращенных URL."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(
        MAX_LENGTH_USERS_SHORT), nullable=False, unique=True
    )
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
    def create(original, short=None, validate=False):
        if short:
            if validate:
                if len(short) > MAX_LENGTH_USERS_SHORT:
                    raise ValueError(INVALID_SHORT)
                if not re.match(SHORT_REGULAR, short):
                    raise ValueError(INVALID_SHORT)
                if URLMap.get(short):
                    raise ValueError(SHORT_EXISTS)
        else:
            short = URLMap.get_unique_short()
        if validate:
            if len(original) > MAX_URL_LENGTH:
                raise ValueError(URL_REQUIRED)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        """Метод модели для извлечения короткого идентификатора."""
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        """Метод модели для получения уникального короткого идентификатора."""
        for _ in range(MAX_GENERATE_ATTEMPTS):
            short = ''.join(random.sample(
                SYMBOLS_STR, MAX_LENGTH_GENERATE_SHORT
            ))
            if not URLMap.get(short):
                return short
        raise ValueError(GENERATE_FAIL)

    def get_full_url(self):
        """
        Метод модели для получения полного URL
        из короткого идентификатора.
        """
        return url_for(
            SHORT_URL_REDIRECT_NAME,
            short=self.short,
            _external=True
        )
