import re

from .constants import MAX_CUSTOM_ID_LENGTH, SHORT_LINK_REGEX
from .error_handlers import CustomValidationError


def validate_data(data):
    """Проверяет данные, переданные в API."""
    if len(data) > MAX_CUSTOM_ID_LENGTH:
        raise CustomValidationError(
            'Указано недопустимое имя для короткой ссылки'
        )
    if not re.fullmatch(SHORT_LINK_REGEX, data):
        raise CustomValidationError(
            'Указано недопустимое имя для короткой ссылки'
        )
