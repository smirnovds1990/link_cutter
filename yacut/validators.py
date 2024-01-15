import string

from .constants import MAX_CUSTOM_ID_LENGTH
from .error_handlers import CustomValidationError


def validate_data(data):
    """Проверяет данные, переданные в API."""
    symbols = string.ascii_letters + string.digits
    if len(data) > MAX_CUSTOM_ID_LENGTH:
        raise CustomValidationError(
            'Указано недопустимое имя для короткой ссылки'
        )
    for char in data:
        if char not in symbols:
            raise CustomValidationError(
                'Указано недопустимое имя для короткой ссылки'
            )
