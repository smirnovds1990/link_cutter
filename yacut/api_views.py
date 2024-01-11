from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('Отсутствует тело запроса.')
    if 'short_link' not in data:
        short_link = get_unique_short_id()
    else:
        short_link = data['short_link']
        if len(short_link) > 16:
            raise InvalidAPIUsage(
                'Вариант короткой ссылки не должен быть больше 16 символов и может содержать только символы - [a-z, A-Z, 0-9]'
            )
    if URLMap.query.filter_by(short=short_link).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    new_link = URLMap(
        original=data['url'],
        short=short_link
    )
    db.session.add(new_link)
    db.session.commit()
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
