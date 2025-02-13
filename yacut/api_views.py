import re
from urllib.parse import urlparse

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id
from settings import (
    MAX_LENGTH_USERS, get_unique_short_id, check_short_link_exists,
    API_ERROR_ID, API_NO_DATA, API_URL_REQUIRED, SHORT_EXISTS,
    API_INVALID_SHORT, API_INVALID_URL, SHORT_REGULAR
)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    API-запрос на получение оригинального URL
    по короткому идентификатору.
    """
    urlmap = check_short_link_exists(model=URLMap, short=short_id)
    if urlmap:
        return jsonify({'url': urlmap.original}), 200
    raise InvalidAPIUsage(API_ERROR_ID, 404)


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    """API-запрос на получение короткой ссылки для полного URL."""
    if not request.data:
        raise InvalidAPIUsage(API_NO_DATA)
    data = request.get_json()
    url = data.get('url', None)
    if not url:
        raise InvalidAPIUsage(API_URL_REQUIRED)
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise InvalidAPIUsage(API_INVALID_URL)
    custom_id = data.get('custom_id', None)
    if custom_id and custom_id not in [None, ""]:
        if check_short_link_exists(model=URLMap, short=custom_id):
            raise InvalidAPIUsage(SHORT_EXISTS)
        if not re.match(SHORT_REGULAR, custom_id) or (
            len(custom_id) > MAX_LENGTH_USERS
        ):
            raise InvalidAPIUsage(API_INVALID_SHORT)
    else:
        custom_id = get_unique_short_id()
    urlmap = URLMap(
        original=url,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({
        'url': urlmap.original,
        'short_link': request.url_root + urlmap.short
    }), 201
