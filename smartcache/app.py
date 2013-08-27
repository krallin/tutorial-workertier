#coding:utf-8
from gevent import monkey
from gevent import pywsgi

from smartcache.backends import Backend
from smartcache.backends.cache.memory import MemoryCache
from smartcache.backends.dispatcher.memory import MemoryDispatcher

monkey.patch_all()


class Handler(object):
    def __init__(self, backend):
        self.backend = backend

    def handle_request(self, env, start_response):
        method = env['REQUEST_METHOD']

        if method not in ("HEAD", "GET"):
            start_response("405 METHOD NOT ALLOWED", [])
            return

        url = env['PATH_INFO']

        if not url.startswith('/') or url == "/":
            start_response('404 Not Found', [])
            return

        key = url[1:]
        value = self.backend.get(key)

        if value is None:
            start_response('203 Non-Authoritative Information', [])
            return

        start_response('200 OK', [('Content-Type', 'text/plain')])
        yield value
        yield "\n"


if __name__ == "__main__":
    print 'Serving on https://127.0.0.1:8443'

    store = {}
    backend = Backend(MemoryCache(store), MemoryDispatcher(store, lambda s: s.swapcase()))
    handler = Handler(backend)
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.serve_forever()
