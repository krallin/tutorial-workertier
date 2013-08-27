#coding:utf-8
import socket

from pymemcache.client import Client, MemcacheError, MemcacheIllegalInputError
from smartcache.backends import BackendUnavailable, InvalidKey
from smartcache.backends.cache import Cache


class MemcachedCache(Cache):
    def __init__(self, host, port):
        self.client = Client((host, port))

    def get(self, key):
        try:
            return self.client.get(key)
        except MemcacheIllegalInputError:
            raise InvalidKey()
        except (MemcacheError, socket.error, socket.timeout):
            raise BackendUnavailable()
