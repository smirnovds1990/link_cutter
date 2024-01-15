from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    MAX_CUSTOM_ID_LENGTH, MIN_CUSTOM_ID_LENGTH, SHORT_LINK_REGEX
)


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(
                regex=SHORT_LINK_REGEX,
                message='Вариант короткой ссылки не должен быть больше 16 символов и может содержать только символы - [a-z, A-Z, 0-9]'
            ),
            Optional(),
            Length(
                MIN_CUSTOM_ID_LENGTH,
                MAX_CUSTOM_ID_LENGTH,
                'Вариант короткой ссылки не должен быть больше 16 символов'
            )
        ]
    )
    submit = SubmitField('Создать')
