
from markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension


def get_path_and_name(path_and_name):
    page_path = path.dirname(path_and_name)
    page_name = path.basename(path_and_name)
    return page_path, page_name


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
