#coding:utf-8
import logging

from gevent import dns

from workertier.backends.cache.memcluster import BaseMemcachedClusterCache


logger = logging.getLogger(__name__)


class DNSMemcachedClusterCache(BaseMemcachedClusterCache):
    def __init__(self, domain, port, timeout):
        super(DNSMemcachedClusterCache, self).__init__(port, timeout)
        self.domain = domain

    def _get_servers_list(self):
        ttl, ips = dns.resolve_ipv4(self.domain)
        # noinspection PyUnresolvedReferences
        return [socket.inet_ntoa(ip) for ip in sorted(ips)]
