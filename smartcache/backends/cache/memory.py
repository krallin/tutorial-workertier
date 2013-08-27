#coding:utf-8
from smartcache.backends.cache import Cache


class MemoryCache(Cache):
    def __init__(self, store):
        """
        :param store: The storage to use for the cache.
        :type store: dict
        """
        self._store = store

    def get(self, key):
        return self._store.get(key)
