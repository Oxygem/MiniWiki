# MiniWiki

MiniWiki is a tiny (<200 line) wiki engine written in Python designed for small(er) wikis (such as [**Stack Setup**](https://stacksetup.com)). Features:

+ Markdown content
+ Inter-page linking (`[[Page Title|/Another/Page]]` or `[[/Another/Page]]`)
+ Index generation based on a path prefix (`[index:/Another]`)
+ Page histories / restore
+ Pluggable authentication backend
+ Custom template support

## Quickstart

1. First, install MiniWiki:

        pip install miniwiki

2. Create a config file ([see config options](./miniwiki/config.py)):

        cat << EOF > config.py
        name = 'My MiniWiki'
        # More, see ./miniwiki/config.py for options
        EOF

3. Run it!

        miniwiki config.py
