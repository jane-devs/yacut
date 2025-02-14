from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from settings import API_ERROR_ID, API_NO_DATA, URL_REQUIRED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    """
    API-запрос на получение оригинального URL
    по короткому идентификатору.
    """
    url_map = URLMap.check_short_link_exists(short)
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(API_ERROR_ID, HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    """API-запрос на получение короткой ссылки для полного URL."""
    if not request.data:
        raise InvalidAPIUsage(API_NO_DATA)
    data = request.get_json()
    url = data.get('url')
    if url in [None, '']:
        raise InvalidAPIUsage(URL_REQUIRED)
    try:
        url_map = URLMap.create(
            original=url,
            short=data.get('custom_id'),
            form_validated=False
        )
    except Exception as e:
        raise InvalidAPIUsage(str(e))
    return jsonify({
        'url': url_map.original,
        'short_link': URLMap.get_full_url(url_map.short)
    }), HTTPStatus.CREATED
