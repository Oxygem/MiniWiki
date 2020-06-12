from uuid import uuid4


def load_config(filename):
    config = get_default_config()

    config_file_vars = {'__file__': filename}
    with open(filename, 'r') as f:
        exec(f.read(), config_file_vars)

    config.update({
        key: value
        for key, value in config_file_vars.items()
        if key in config
    })

    return config


def get_default_config():
    return {
        # Basics
        'debug': False,
        'secret_key': f'{uuid4()}',
        'name': 'MiniWiki',
        'database': 'sqlite:///miniwiki.db',

        # Custom template & static
        'template_folder': None,
        'static_folder': None,

        # Auth backend + settings
        'auth_backend': 'miniwiki.auth.AnonymousAuthBackend',
        'auth_backend_settings': {},

        # Cache backend + settings
        'cache_backend': 'miniwiki.cache.NoCacheBackend',
        'cache_backend_settings': {},
    }
