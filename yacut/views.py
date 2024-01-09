import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    """Формирует короткую ссылку, если пользователь не ввёл свой вариант."""
    symbols = string.ascii_letters + string.digits
    domain = 'https://127.0.0.5000/'
    random_link = ''.join(random.choice(symbols) for _ in range(6))
    generated_link = domain + random_link
    if URLMap.query.filter_by(short=generated_link).first() is not None:
        return get_unique_short_id()
    return generated_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
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
        return redirect(url_for('link_view', id=new_link.id))
    return render_template('index.html', form=form)


@app.route('/<int:id>')
def link_view(id):
    form = URLForm()
    new_link = URLMap.query.get_or_404(id)
    flash(f'{new_link.short}', 'created')
    return render_template('index.html', new_link=new_link, form=form)
