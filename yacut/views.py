from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.forms import MainForm
from yacut.models import URLMap
from settings import check_short_link_exists


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        short = form.custom_id.data
        return render_template(
            'index.html',
            form=form,
            short_link=URLMap.get_or_create(
                original=form.original_link.data,
                short=short if short else None
            )['short_link']
        )
    except Exception as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_original(short):
    url_map = check_short_link_exists(model=URLMap, short=short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
