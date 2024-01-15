from flask import redirect, request, render_template

from . import app
from .error_handlers import LinkCreationError
from .forms import URLForm
from .models import URLMap
from .utils import create_new_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Представление для главной страницы."""
    form = URLForm()
    new_link = None
    error_message = None
    if form.validate_on_submit():
        try:
            new_link = create_new_link(
                original=form.original_link.data, short=form.custom_id.data
            )
        except LinkCreationError as error:
            error_message = error.message
            return render_template(
                'index.html', form=form, error_message=error_message
            )
    full_url = request.host_url + new_link.short if new_link else None
    return render_template('index.html', form=form, new_link=full_url)


@app.route('/<string:short>')
def redirect_view(short):
    """Редирект после создания ссылки."""
    new_link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(new_link.original)
