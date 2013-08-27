#coding:utf-8
import logging

from gevent import pywsgi
from gevent.event import Event

from smartcache.config import ConfigLoader
from smartcache.handler import Handler


CONFIG_PATH = "config.ini"
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    print 'Serving on https://127.0.0.1:8443'
    config = ConfigLoader(CONFIG_PATH)

    handler = Handler(config.cache(), config.dispatcher())
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.start()

    # Just wait until the end of time now.
    event = Event()
    event.wait()
