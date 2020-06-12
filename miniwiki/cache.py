from pymemcache import serde
from pymemcache.client.base import PooledClient


class NoCacheBackend(object):
    def __init__(self, config):
        pass

    def get(self, key):
        return None

    def set(self, key, value):
        return True


class PymemcacheCacheBackend(NoCacheBackend):
    def __init__(self, config):
        cache_settings = config['cache_backend_settings']

        host = cache_settings.get('host')
        port = cache_settings.get('port')

        if not host or not port:
            raise ValueError((
                'Must provide `config.cache_backend_settings.[host|port]`'
                ' with `PymemcacheCacheBackend!'
            ))

        self.host = host
        self.port = port
        self._make_client()

    def _make_client(self):
        self.client = PooledClient(
            (self.host, self.port),
            serde=serde.pickle_serde,
        )

    def get(self, key):
        try:
            return self.client.get(key)
        except Exception as e:
            print(f'FAILED CACHE GET: {e.__class__.__name__}({e.args})')

    def set(self, key, value):
        try:
            return self.client.set(key, value)
        except Exception as e:
            print(f'FAILED CACHE SET: {e.__class__.__name__}({e.args})')

    def delete(self, key):
        try:
            return self.client.delete(key)
        except Exception as e:
            print(f'FAILED CACHE DELETE: {e.__class__.__name__}({e.args})')
