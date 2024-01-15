import random
import string

from . import db
from .constants import GENERATED_LINK_LENGTH
from .error_handlers import LinkCreationError
from .models import URLMap
from .validators import validate_data


def get_link_by_short_id(short_id):
    """Получает объект из БД по короткой ссылке."""
    return URLMap.query.filter_by(short=short_id).first()


def get_unique_short_id():
    """Формирует короткую ссылку, если пользователь не ввёл свой вариант."""
    symbols = string.ascii_letters + string.digits
    random_link = ''.join(
        random.choice(symbols) for _ in range(GENERATED_LINK_LENGTH)
    )
    if get_link_by_short_id(random_link) is not None:
        return get_unique_short_id()
    return random_link


def create_obj_and_add_to_db(original, short):
    """Создает объект URLMap и сохраняет изменения в БД."""
    new_link = URLMap(
        original=original,
        short=short
    )
    db.session.add(new_link)
    db.session.commit()
    return new_link


def create_new_link(original, short):
    """
    Создает короткую ссылку из полученных данных о длинной и короткой ссылках
    """
    if not short or short == '':
        short = get_unique_short_id()
    else:
        validate_data(short)
    if get_link_by_short_id(short) is not None:
        raise LinkCreationError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    new_link = create_obj_and_add_to_db(
        original=original, short=short
    )
    return new_link
