import string

SYMBOLS_STR = string.ascii_letters + string.digits
SHORT_REGULAR = f'^[{SYMBOLS_STR}]+$'

MAX_LENGTH_GENERATE_SHORT = 6
MAX_LENGTH_USERS_SHORT = 16
MAX_URL_LENGTH = 2048

API_ERROR_SHORT = 'Указанный id не найден'
API_NO_DATA = 'Отсутствует тело запроса'
URL_REQUIRED = '"url" является обязательным полем!'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_URL = 'Указан невалидный URL.'
CUSTOM_ID_DESCRIPTION = 'Желаемая короткая ссылка'
DATA_REQUIRED = 'Обязательное поле'
ORIGINAL_DESCRIPTION = 'Вставьте ссылку'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
SUBMIT_BUTTON_TEXT = 'Создать'
