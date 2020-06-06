from os import path

from flask import render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from miniwiki.util import add_wiki_indexes, add_wiki_links, markdownify


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
        html = add_wiki_indexes(Page, html)
        html = add_wiki_links(Page, html)
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
