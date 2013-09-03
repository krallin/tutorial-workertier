#coding:utf-8
import random
import logging
import zlib

from gevent import socket, dns
from workertier.backends import BackendUnavailable

from workertier.backends.cache import Cache
from workertier.backends.cache.memcached import MemcachedCache


logger = logging.getLogger(__name__)


class DomainClusteredMemcachedCache(Cache):
    def __init__(self, domain, port, timeout):
        self.domain = domain
        self.port = port
        self.timeout = timeout

        self._ips = []
        self._clients = {}

    def _refresh_server_list(self):
        logger.debug("Refreshing Memcached server list")
        ttl, ips = dns.resolve_ipv4(self.domain)
        # noinspection PyUnresolvedReferences
        self._ips = [socket.inet_ntoa(ip) for ip in sorted(ips)]

    def _get_server(self, key):
        # Naive, low-performance implementation
        assert self._ips, "_find_server should not have been called with self._ips == []"
        return self._ips[zlib.crc32(key) % len(self._ips)]

    def _get_cache(self, key):
        server = self._get_server(key)
        if  server not in self._clients:
            logger.debug("Creating new client for %s", server)
            self._clients[server] = MemcachedCache(server, self.port, self.timeout)
        return self._clients[server]

    def get_cache(self, key):
        # Refresh our servers list 10% of the time (we should use signals)
        if random.random() < 0.1 or not self._ips:
            self._refresh_server_list()

        if not self._ips:
            raise BackendUnavailable("No servers for {0}".format(self.domain))

        return self._get_cache(key)

    def get(self, key):
        return self.get_cache(key).get(key)

    def set(self, key, value):
        return self.get_cache(key).set(key, value)
