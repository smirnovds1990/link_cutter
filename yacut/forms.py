from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(
                regex='^[a-zA-Z0-9]{1,16}$',
                message='Вариант короткой ссылки не должен быть больше 16 символов и может содержать только символы - [a-z, A-Z, 0-9]'
            ),
            Optional(),
            Length(
                1, 16, 'Вариант короткой ссылки не должен быть больше 16 символов'
            )
        ]
    )
    submit = SubmitField('Создать')
