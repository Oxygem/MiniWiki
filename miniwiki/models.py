import re

from os import path

from flask import render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from miniwiki.util import get_path_and_name, markdownify

INDEX_REGEX = re.compile(r'\[index\:([\/\ \w]+)\]')
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

    @property
    def url(self):
        return url_for('get_or_edit_page', location=path.join(self.path, self.name))

    def __str__(self):
        return path.join(self.path, self.name)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def render_toc_and_content(self):
        toc, html = markdownify(self.content)
        html = self.add_wiki_indexes(html)
        html = self.add_wiki_links(html)
        return toc, html

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

    def add_wiki_indexes(self, html):
        def make_index(value):
            page_path = value.group(1)
            pages = Page.query.filter_by(path=page_path)
            return render_template('macro/index_links.html', pages=pages)

        return re.sub(INDEX_REGEX, make_index, html)

    def add_wiki_links(self, html):
        def make_link(value):
            page_path, page_name = get_path_and_name(value)
            page = Page.query.get((page_path, page_name))
            if page:
                return f'<a href="{page.url}">{page.title}</a>'
            return f'<a href="{page_path}{page_name}">{page_path}{page_name}</a>'

        return re.sub(LINK_REGEX, make_link, html)


class Page(db.Model, PageMixin):
    __tablename__ = 'page'

    path = db.Column(db.String(300, collation='NOCASE'), primary_key=True)
    name = db.Column(db.String(300, collation='NOCASE'), primary_key=True)

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
