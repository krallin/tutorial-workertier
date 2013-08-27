#coding:utf-8
import logging

from gevent import pywsgi
from gevent.event import Event

from smartcache.app import Handler
from smartcache.backends.cache.memcached import MemcachedCache
from smartcache.backends.dispatcher.rabbitmq import RabbitMQDispatcher

logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    print 'Serving on https://127.0.0.1:8443'
    handler = Handler(MemcachedCache("localhost", 11211), RabbitMQDispatcher("localhost", 5672, "/", "guest", "guest", "myqueue"))
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.start()

    # Just wait until the end of time now.
    event = Event()
    event.wait()
