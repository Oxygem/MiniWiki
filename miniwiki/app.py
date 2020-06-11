from importlib import import_module
from os import path
from time import time

from flask import abort, Flask, redirect, render_template, request, url_for
from jinja2 import FileSystemLoader
from werkzeug.exceptions import HTTPException

from miniwiki.models import db, Page
from miniwiki.util import get_path_and_name


def make_app(config):
    wiki_name = config['name']

    app = Flask('miniwiki', static_folder=config['static_folder'])
    app.debug = config['debug']
    app.secret_key = config['secret_key']

    # Templates
    #

    template_folders = []

    if config['template_folder']:
        template_folders.append(config['template_folder'])

    this_dir = path.dirname(__file__)
    template_folders.append(path.join(this_dir, 'templates'))

    app.jinja_loader = FileSystemLoader(template_folders)

    # Database
    #

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'timeout': 30}}
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']

    db.init_app(app)

    # Auth?
    #

    auth_module, auth_cls = config['auth_backend'].rsplit('.', 1)
    auth_module = import_module(auth_module)
    auth_cls = getattr(auth_module, auth_cls)
    auth = auth_cls(config)

    if auth.get_login:
        app.route('/login', methods=('GET',))(auth.get_login)

    if auth.post_login:
        app.route('/login', methods=('POST',))(auth.post_login)

    if auth.get_logout:
        app.route('/logout', methods=('GET',))(auth.get_logout)

    # Wiki view
    #

    @app.route('/', defaults={'location': ''}, methods=('GET', 'POST'))
    @app.route('/<path:location>', methods=('GET', 'POST'))
    def get_or_edit_page(location):
        start_time = time()

        if location.endswith('/'):
            return redirect(url_for('get_or_edit_page', location=location[:-1]))

        path_and_name = f'/{location}'
        page_path, page_name = get_path_and_name(path_and_name)

        page = Page.query.get((page_path, page_name))
        status = 200 if page else 404

        if request.method == 'GET':
            template = 'page.html'

            if request.args.get('edit') == '':
                if auth.is_logged_in():
                    template = 'edit_page.html'
                else:
                    abort(403)

            return render_template(
                template,
                status=status,
                page=page,
                page_path=page_path,
                path_and_name=path_and_name,
                exists=page is not None,
                page_url=url_for('get_or_edit_page', location=location),
                wiki_name=wiki_name,
                page_generate_time=round(time() - start_time, 5),
                is_logged_in=auth.is_logged_in(),
                logout_url=url_for('get_logout') if auth.get_logout else None,
                login_url=url_for('get_login') if auth.get_login else None,
            ), status

        if page:
            page_log = page.create_page_log()
            db.session.add(page_log)
        else:
            page = Page()
            page.path = page_path
            page.name = page_name

        page.update(
            title=request.form['title'],
            content=request.form['content'],
            sidebar=request.form['sidebar'],
            description=request.form['description'],
            keywords=request.form['keywords'],
            sidebar_toc=request.form.get('sidebar_toc') == 'on',
        )

        db.session.add(page)
        db.session.commit()

        return redirect(url_for('get_or_edit_page', location=location))

    # Error view
    #

    @app.errorhandler(HTTPException)
    def get_error(e):
        return render_template(
            'error.html',
            status=e.code,
            name=e.name,
            description=e.description,
        ), e.code

    return app
