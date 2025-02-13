from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from settings import (
    check_short_link_exists,
    API_ERROR_ID, API_NO_DATA, API_URL_REQUIRED
)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    API-запрос на получение оригинального URL
    по короткому идентификатору.
    """
    url_map = check_short_link_exists(model=URLMap, short=short_id)
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(API_ERROR_ID, HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    """API-запрос на получение короткой ссылки для полного URL."""
    if not request.data:
        raise InvalidAPIUsage(API_NO_DATA)
    data = request.get_json()
    url = data.get('url', None)
    if not url:
        raise InvalidAPIUsage(API_URL_REQUIRED)
    url_map = URLMap.get_or_create(
        original=url, short=data.get('custom_id', None)
    )
    return jsonify(url_map), HTTPStatus.CREATED
