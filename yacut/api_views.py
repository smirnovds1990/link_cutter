import string

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    symbols = string.ascii_letters + string.digits
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
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        for char in custom_id:
            if char not in symbols:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    new_link = URLMap(
        original=data['url'],
        short=custom_id
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
