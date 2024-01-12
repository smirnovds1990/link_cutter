import random
import string

from . import db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def get_unique_short_id():
    """Формирует короткую ссылку, если пользователь не ввёл свой вариант."""
    symbols = string.ascii_letters + string.digits
    random_link = ''.join(random.choice(symbols) for _ in range(6))
    if URLMap.query.filter_by(short=random_link).first() is not None:
        return get_unique_short_id()
    return random_link


def validate_data(data):
    """Проверяет данные, переданные в API."""
    symbols = string.ascii_letters + string.digits
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
    return custom_id


def create_obj_and_add_to_DB(original, short):
    """Создает объект URLMap и сохраняет изменения в БД."""
    new_link = URLMap(
        original=original,
        short=short
    )
    db.session.add(new_link)
    db.session.commit()
    return new_link
