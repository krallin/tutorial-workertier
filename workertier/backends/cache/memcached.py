#coding:utf-8
import logging
import socket

import gevent.socket
from pymemcache.client import Client, MemcacheError, MemcacheIllegalInputError

from workertier.backends import BackendUnavailable, InvalidKey
from workertier.backends.cache import Cache


logger = logging.getLogger(__name__)



class MemcachedCache(Cache):
    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.client = Client((self.host, self.port), connect_timeout=timeout, timeout=timeout, socket_module=gevent.socket)

    def _invoke_command(self, command, *args, **kwargs):
        try:
            return command(*args, **kwargs)
        except MemcacheIllegalInputError:
            raise InvalidKey()
        except (MemcacheError, socket.error, socket.timeout) as e:
            logger.warning("Connection error (%s:%s): %s", self.host, self.port, e)
            raise BackendUnavailable()

    def get(self, key):
        return self._invoke_command(self.client.get, key)

    def set(self, key, value):
        return self._invoke_command(self.client.set, key, value)
