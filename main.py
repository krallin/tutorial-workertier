#coding:utf-8
from gevent import pywsgi

from smartcache.app import Handler
from smartcache.backends import Backend
from smartcache.backends.cache.memory import MemoryCache
from smartcache.backends.dispatcher.memory import MemoryDispatcher


if __name__ == "__main__":
    print 'Serving on https://127.0.0.1:8443'

    store = {}
    backend = Backend(MemoryCache(store), MemoryDispatcher(store, lambda s: s.swapcase()))
    handler = Handler(backend)
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.serve_forever()
