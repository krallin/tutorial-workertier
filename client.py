#coding:utf-8
import logging

from gevent import monkey; monkey.patch_all()
from gevent.event import Event

from smartcache.consumer import Consumer
from smartcache.config import ConfigLoader


CONFIG_PATH = "config.ini"
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    config = ConfigLoader(CONFIG_PATH)
    consumer = Consumer(config.cache(), config.dispatcher())
    consumer.start()

    # Just wait until the end of time now.
    event = Event()
    event.wait()
