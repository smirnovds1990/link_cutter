from flask import redirect, request, render_template

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import create_new_link, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Представление для главной страницы."""
    form = URLForm()
    new_link = None
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        new_link = create_new_link(
            original=form.original_link.data, short=short
        )
        if new_link is None:
            return render_template('index.html', form=form)
    full_url = request.host_url + new_link.short if new_link else None
    return render_template('index.html', form=form, new_link=full_url)


@app.route('/<string:short>')
def redirect_view(short):
    """Редирект после создания ссылки."""
    new_link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(new_link.original)
