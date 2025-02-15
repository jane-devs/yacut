from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import YacutException
from yacut.models import URLMap
from yacut.constants import API_ERROR_SHORT, API_NO_DATA, URL_REQUIRED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    """
    API-запрос на получение оригинального URL
    по короткому идентификатору.
    """
    url_map = URLMap.get(short)
    if url_map:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise YacutException(API_ERROR_SHORT, HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    """API-запрос на получение короткой ссылки для полного URL."""
    if not request.data:
        raise YacutException(API_NO_DATA)
    data = request.get_json()
    if 'url' not in data or not data['url']:
        raise YacutException(URL_REQUIRED)
    url = data.get('url')
    try:
        return jsonify({
            'url': data['url'],
            'short_link': URLMap.create(
                original=url,
                short=data.get('custom_id'),
                validate=True
            ).get_full_url()
        }), HTTPStatus.CREATED
    except ValueError as e:
        raise YacutException(str(e))
