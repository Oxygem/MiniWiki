import json

import click

from cheroot import wsgi

from miniwiki.app import make_app
from miniwiki.config import load_config
from miniwiki.models import db, Page


def import_pages(import_filename):
    with open(import_filename, 'r') as f:
        data = json.load(f)

    for page_data in data:
        page = Page()
        for key, value in page_data.items():
            setattr(page, key, value)

        db.session.add(page)
    db.session.commit()


def export_pages(export_filename):
    pages = []

    for page in Page.query.all():
        pages.append(page.to_dict())

    with open(export_filename, 'w') as f:
        json.dump(pages, f)


@click.command()
@click.option('import_filename', '--import', type=click.Path(exists=True))
@click.option('export_filename', '--export', type=click.Path(exists=False))
@click.option('--initdb', is_flag=True, default=False)
@click.option('--host', default='0.0.0.0')
@click.option('--port', type=int, default=5000)
@click.argument('config_filename', type=click.Path(exists=True))
def start_miniwiki(
    import_filename,
    export_filename,
    initdb,
    host,
    port,
    config_filename,
):
    config = load_config(config_filename)
    app = make_app(config)

    if initdb:
        with app.app_context():
            db.create_all()
        click.echo('Database initialized!')
        return

    if import_filename:
        with app.app_context():
            return import_pages(import_filename)

    if export_filename:
        with app.app_context():
            return export_pages(export_filename)

    if config['debug']:
        app.run(host=host, port=port)
    else:
        server = wsgi.Server((host, port), app)
        server.start()
