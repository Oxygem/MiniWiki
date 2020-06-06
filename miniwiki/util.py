import re

from os import path

from flask import render_template
from markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension


def get_path_and_name(path_and_name):
    page_path = path.dirname(path_and_name)
    page_name = path.basename(path_and_name)
    return page_path, page_name


INDEX_REGEX = re.compile(r'\[index\:([\/a-zA-Z0-9]+)\]')
LINK_REGEX = re.compile(r'\[\[([\/a-zA-Z0-9|]+)\]\]')


def add_wiki_indexes(page_cls, html):
    def make_index(value):
        page_path = value.group(1)
        pages = page_cls.query.filter_by(path=page_path)
        return render_template('macro/index_links.html', pages=pages)

    return re.sub(INDEX_REGEX, make_index, html)


def add_wiki_links(page_cls, html):
    def make_link(value):
        page_path, page_name = get_path_and_name(value.group(1))
        page = page_cls.query.get((page_path, page_name))
        if page:
            return f'<a href="{page.url}">{page.title}</a>'
        return f'<a href="{page_path}{page_name}">{page_path}{page_name}</a>'

    return re.sub(LINK_REGEX, make_link, html)


def markdownify(text):
    md = Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.nl2br',  # turn newlines into breaks
        'markdown.extensions.sane_lists',
        'markdown.extensions.toc',
        LinkifyExtension(),  # pass class for pyinstaller to bundle
    ])
    html = md.convert(text)
    return md.toc, html
