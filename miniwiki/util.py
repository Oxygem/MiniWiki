from os import path, sep

from markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension


def capitalize_first_letter(string):
    if string:
        return string[0].upper() + string[1:]
    return ''


def get_path_and_name(path_and_name):
    page_path = sep.join([
        capitalize_first_letter(bit)
        for bit in path.dirname(path_and_name).split(sep)
    ])
    page_name = capitalize_first_letter(path.basename(path_and_name))
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


def split_path_locations(path_name):
    path_name = path_name[1:]
    path_bits = path_name.split(sep)
    paths = [('/', '/')]

    for i, bit in enumerate(path_bits, 1):
        if not bit:
            continue

        sub_path = f'/{sep.join(path_bits[:i])}'
        paths.append((sub_path, capitalize_first_letter(bit)))

    return paths
