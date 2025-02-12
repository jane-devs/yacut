from random import choice

from flask import flash, redirect, render_template

from yacut import app, db
from yacut.forms import MainForm
from yacut.models import URLMap
from settings import MAX_LENGTH, SYMBOLS_STR


def get_unique_short_id():
    while True:
        yield ''.join(choice(SYMBOLS_STR) for _ in range(MAX_LENGTH))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_link = form.custom_id.data
    if not short_link:
        short_link = next(get_unique_short_id())
    if URLMap.query.filter_by(short=short_link).first() is not None:
        flash('Такая ссылка уже занята!')
        return render_template('index.html', form=form)
    url = URLMap(
        original=form.original_link.data,
        short=short_link,
    )
    db.session.add(url)
    db.session.commit()
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<short>')
def redirect_to_original(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map:
        return redirect(url_map.original)
    flash('Ссылка не найдена!')
    form = MainForm()
    return render_template('index.html', form=form)
