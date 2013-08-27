#coding:utf-8
import logging

from gevent import monkey;  monkey.patch_all()
from gevent.event import Event

from smartcache.backends.cache.memcached import MemcachedCache
from smartcache.backends.dispatcher.rabbitmq import RabbitMQDispatcher
from smartcache.consumer import Consumer


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    memcached = MemcachedCache("localhost", 11211)
    rabbitmq = RabbitMQDispatcher("localhost", 5672, "/", "guest", "guest", "myqueue")

    consumer = Consumer(memcached, rabbitmq)
    consumer.start()

    # Just wait until the end of time now.
    event = Event()
    event.wait()
