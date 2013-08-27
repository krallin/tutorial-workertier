#coding:utf-8
# Really messy right now
from gevent import monkey; monkey.patch_all()
from gevent.event import Event


import logging

from smartcache.backends.cache.memcached import MemcachedCache
from smartcache.backends.dispatcher.rabbitmq import RabbitMQDispatcher


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


NUM_GTHREADS = 5


if __name__ == "__main__":
    memcached = MemcachedCache("localhost", 11211)
    rabbitmq = RabbitMQDispatcher("localhost", 5672, "/", "guest", "guest", "myqueue")

    def consumer(message):
        logger.debug("Received a new message: '%s'", message.body)
        key = message.body
        memcached.set(key, key.swapcase())

    for _ in xrange(NUM_GTHREADS):
        rabbitmq.consume(consumer)

    # Just wait until the end of time now.
    event = Event()
    event.wait()
