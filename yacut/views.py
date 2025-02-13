from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import MainForm
from yacut.models import URLMap
from settings import get_unique_short_id, check_short_link_exists, SHORT_EXISTS


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if check_short_link_exists(model=URLMap, short=short) is not None:
            flash(SHORT_EXISTS)
            return render_template('index.html', form=form)
        if not short:
            short = get_unique_short_id()
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, short_link=short)
    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_original(short):
    url_map = check_short_link_exists(model=URLMap, short=short)
    if url_map:
        return redirect(url_map.original)
    abort(404)
