from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .utils import (
    create_new_link, get_link_by_short_id, get_unique_short_id,
    validate_data
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if (
        'custom_id' not in data or data['custom_id'] == ''
        or data['custom_id'] is None
    ):
        custom_id = get_unique_short_id()
    else:
        custom_id = data['custom_id']
    validate_data(custom_id)
    new_link = create_new_link(original=data['url'], short=custom_id)
    full_url = request.host_url + new_link.short if new_link else None
    return jsonify(
        {"url": new_link.original, "short_link": full_url}
    ), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по id короткой ссылки."""
    link = get_link_by_short_id(short_id)
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({"url": link.original}), 200
