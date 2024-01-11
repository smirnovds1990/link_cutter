import random
import string

from flask import flash, redirect, request, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    """Формирует короткую ссылку, если пользователь не ввёл свой вариант."""
    symbols = string.ascii_letters + string.digits
    random_link = ''.join(random.choice(symbols) for _ in range(6))
    if URLMap.query.filter_by(short=random_link).first() is not None:
        return get_unique_short_id()
    return random_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Представление для главной страницы."""
    form = URLForm()
    new_link = None
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'error'
            )
            return render_template('index.html', form=form)
        new_link = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(new_link)
        db.session.commit()
    full_url = request.host_url + new_link.short if new_link else None
    return render_template('index.html', form=form, new_link=full_url)


@app.route('/<string:short>')
def redirect_view(short):
    """Редирект после создания ссылки."""
    new_link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(new_link.original)
