#coding:utf-8
import logging
from gevent import pywsgi

from smartcache.app import Handler
from smartcache.backends import Backend

from smartcache.backends.cache.memory import MemoryCache
from smartcache.backends.dispatcher.memory import MemoryDispatcher

from smartcache.backends.cache.memcached import MemcachedCache
from smartcache.backends.dispatcher.rabbitmq import RabbitMQDispatcher

logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    print 'Serving on https://127.0.0.1:8443'

    store = {}
    #backend = Backend(MemoryCache(store), MemoryDispatcher(store, lambda s: s.swapcase()))
    backend = Backend(MemcachedCache("localhost", 11211), RabbitMQDispatcher("localhost", 5672, "/", "guest", "guest", "myqueue"))
    handler = Handler(backend)
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.serve_forever()
