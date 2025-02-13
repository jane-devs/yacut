import os
from random import choice

MAX_LENGTH_GENERATE = 6
MAX_LENGTH_USERS = 16
SYMBOLS_STR = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
API_ERROR_ID = 'Указанный id не найден'
API_NO_DATA = 'Отсутствует тело запроса'
API_URL_REQUIRED = '\"url\" является обязательным полем!'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
API_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
API_INVALID_URL = 'Указан невалидный URL.'
SHORT_REGULAR = r'^[a-zA-Z0-9]+$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


def get_unique_short_id():
    return ''.join(choice(SYMBOLS_STR) for _ in range(MAX_LENGTH_GENERATE))


def check_short_link_exists(model, short):
    return model.query.filter_by(short=short).first()
