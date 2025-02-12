from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.views import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def add_short_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap:
        return jsonify({'url': urlmap.original}), 200
    raise InvalidAPIUsage('Указанный id не найден')


# @app.route('/api/id/', methods=['POST'])
# def get_original_link():
#     # Получение данных из запроса в виде словаря:
#     data = request.get_json()
#     if 'title' not in data or 'text' not in data:
#         # ...то возвращаем сообщение об ошибке в формате JSON и код 400:
#         raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
#     if Opinion.query.filter_by(text=data['text']).first() is not None:
#         # ...возвращаем сообщение об ошибке в формате JSON
#         # и статус-код 400:
#         raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
#     # Создание нового пустого экземпляра модели:
#     opinion = Opinion()
#     # Наполнение экземпляра данными из запроса:
#     opinion.from_dict(data)
#     # Добавление новой записи в сессию:
#     db.session.add(opinion)
#     # Сохранение изменений:
#     db.session.commit()
#     return jsonify({'opinion': opinion.to_dict()}), 201