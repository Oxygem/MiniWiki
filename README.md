# MiniWiki

MiniWiki is a tiny wiki engine written in Python designed for small(er) wikis (such as [**Stack Setup**](https://stacksetup.com)). Features:

+ Markdown content
+ Inter-page linking (`[[Page Title|/Another/Page]]` or `[[/Another/Page]]`)
+ Index generation based on a path prefix (`[index:/Another]`)
+ Page history log (WIP)
+ Pluggable authentication backend
+ Custom template support

## Quickstart

1. First, install MiniWiki:

        pip install miniwiki

2. Create a Python config file ([see config options](./miniwiki/config.py)):

        # config.py
        name = 'My MiniWiki'
        database = 'sqlite:///my-miniwiki.db'

3.  Initialize the database

        miniwiki config.py --initdb

4. Run it!

        miniwiki config.py

## Configuration

### Database

The database variable can be any valid [SQLAlchemy database URI](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls).

### Authentication

By default MiniWiki instances allow public editing. The authentication backend can be set via config variable `auth_backend`. MiniWiki comes with two builtin backends:

#### `AnonymousAuthBackend`

Allows anyone to edit the wiki, usage:

```py
auth_backend = 'miniwiki.auth.AnonymousAuthBackend'
```

#### ``SimpleAuthBackend``

Allows a hard-coded list of users to edit the wiki, usage:

```py
auth_backend = 'miniwiki.auth.SimpleAuthBackend'
auth_backend_settings = {
    'users': {
        'USERNAME': 'HASHED_PASSWORD',
    },
}
```

You will need to hash the passwords like so:

```py
from bcrypt import hashpw, gensalt
hashed_password = hashpw(b'PASSWORD', gensalt(N_BCRYPT_ROUNDS))
```
