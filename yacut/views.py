from flask import flash, redirect, request, render_template

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import create_obj_and_add_to_DB, get_unique_short_id


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
        new_link = create_obj_and_add_to_DB(
            original=form.original_link.data, short=short
        )
    full_url = request.host_url + new_link.short if new_link else None
    return render_template('index.html', form=form, new_link=full_url)


@app.route('/<string:short>')
def redirect_view(short):
    """Редирект после создания ссылки."""
    new_link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(new_link.original)
