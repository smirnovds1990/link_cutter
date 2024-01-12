from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import create_obj_and_add_to_DB, validate_data


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    data = request.get_json()
    custom_id = validate_data(data)
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    new_link = create_obj_and_add_to_DB(original=data['url'], short=custom_id)
    full_url = request.host_url + new_link.short if new_link else None
    return jsonify(
        {"url": new_link.original, "short_link": full_url}
    ), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинальной ссылки по id короткой ссылки."""
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({"url": link.original}), 200
