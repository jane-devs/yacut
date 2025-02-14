from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from wtforms.validators import ValidationError

from yacut import app
from yacut.forms import MainForm
from yacut.models import URLMap


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
            short_link=URLMap.get_full_url(
                URLMap.create(
                    original=form.original_link.data,
                    short=short,
                    form_validated=True
                ).short
            ))
    except ValidationError as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_original(short):
    url_map = URLMap.check_short_link_exists(short=short)
    if url_map:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)


@app.route('/docs', methods=['GET'])
def documentation():
    return render_template('docs.html')
