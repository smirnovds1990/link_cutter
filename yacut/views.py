from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
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
    new_link = URLMap.query.get_or_404(id)
    return render_template('link.html', new_link=new_link)
