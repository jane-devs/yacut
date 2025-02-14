import os

API_ERROR_ID = 'Указанный id не найден'
API_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
API_INVALID_URL = 'Указан невалидный URL.'
API_NO_DATA = 'Отсутствует тело запроса'
CUSTOM_ID_DESCRIPTION = 'Желаемая короткая ссылка'
DATA_REQUIRED = 'Обязательное поле'
MAX_LENGTH_GENERATE = 6
MAX_LENGTH_USERS = 16
MAX_URL_LENGTH = 128
ORIGINAL_DESCRIPTION = 'Вставьте ссылку'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_REGULAR = r'^[a-zA-Z0-9]+$'
SUBMIT_BUTTON_TEXT = 'Создать'
SYMBOLS_STR = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
URL_REQUIRED = '\"url\" является обязательным полем!'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
