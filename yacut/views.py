from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first() is not None:
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'error'
            )
            return render_template('index.html', form=form)
        new_link = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
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
