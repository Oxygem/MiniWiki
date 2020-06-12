import re

from os import path

from flask import render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from miniwiki.util import get_path_and_name, markdownify

REDIRECT_REGEX = re.compile(r'\[redirect\:([\/\ \w]+)\]')
INDEX_REGEX = re.compile(r'\[index\:([\/\ \w]*)\]')
LINK_REGEX = re.compile(r'\[\[([\/\|\ \w]+)\]\]')


db = SQLAlchemy()


class PageMixin(object):
    __tablename__ = 'page'

    path = db.Column(db.String(300, collation='NOCASE'), primary_key=True)
    name = db.Column(db.String(300, collation='NOCASE'), primary_key=True)

    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)

    sidebar_toc = db.Column(db.Boolean, nullable=False, default=False)
    sidebar = db.Column(db.Text, nullable=True)

    description = db.Column(db.String(300), nullable=True)
    keywords = db.Column(db.String(300), nullable=True)

    class PageRedirectError(Exception):
        def __init__(self, location):
            self.location = location

    @property
    def url(self):
        return url_for('get_or_edit_page', location=path.join(self.path, self.name))

    @property
    def cache_key(self):
        return f'{self}'

    def __str__(self):
        return path.join(self.path, self.name)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def render_toc_and_content(self, do_redirects=True):
        cached = self.cache.get(self.cache_key)
        if cached:
            return cached, True

        if do_redirects:
            self.find_raise_redirect(self.content)

        toc, html = markdownify(self.content)
        html = self.add_wiki_indexes(html)
        html = self.add_wiki_links(html)

        self.cache.set(self.cache_key, (toc, html))
        return (toc, html), False

    def render_sidebar(self):
        if not self.sidebar:
            return ''

        _, html = markdownify(self.sidebar)
        return html

    def render_meta(self):
        return render_template(
            'macro/page_meta.html',
            description=self.description,
            keywords=self.keywords,
        )

    def find_raise_redirect(self, html):
        match = REDIRECT_REGEX.search(html)
        if match:
            location = match.group(1)
            raise self.PageRedirectError(location=location)

    def add_wiki_indexes(self, html):
        def make_index(value):
            page_path = value.group(1)
            if not page_path:
                page_path = path.join(self.path, self.name)
            pages = Page.query.filter_by(path=page_path)
            return render_template('macro/index_links.html', pages=pages)

        return re.sub(INDEX_REGEX, make_index, html)

    def add_wiki_links(self, html):
        def make_link(value):
            value = value.group(1)
            title = None

            if '|' in value:
                title, value = value.split('|', 1)

            page_path, page_name = get_path_and_name(value)
            url = path.join(page_path, page_name)

            page = Page.query.get((page_path, page_name))
            if page:
                title = page.title
                url = page.url

            if title is None:
                title = url

            return f'<a href="{url}">{title}</a>'

        return re.sub(LINK_REGEX, make_link, html)


class Page(db.Model, PageMixin):
    __tablename__ = 'page'

    path = db.Column(db.String(300, collation='NOCASE'), primary_key=True)
    name = db.Column(db.String(300, collation='NOCASE'), primary_key=True)

    def update(self, *args, **kwargs):
        super(Page, self).update(*args, **kwargs)
        self.cache.delete(self.cache_key)

    def create_page_log(self):
        columns = self.__table__.columns.keys()

        page_log = PageLog()
        page_log.update(**{
            key: getattr(self, key)
            for key in columns
        })

        return page_log


class PageLog(db.Model, PageMixin):
    __tablename__ = 'page_log'

    id = db.Column(db.Integer, primary_key=True)

    path = db.Column(db.String(300, collation='NOCASE'), index=True)
    name = db.Column(db.String(300, collation='NOCASE'), index=True)
