#coding:utf-8
import random
import gevent
from gevent.coros import Semaphore

from haigha.connection import Connection as HaighaConnection
from haigha.exceptions import ChannelClosed
from haigha.message import Message

from smartcache.backends.dispatcher import Dispatcher


class Connection(object):
    def __init__(self, host, port, vhost, user, password, queue):
        self._conn_kwargs = {
            "host": host,
            "port": port,
            "vhost": vhost,
            "user": user,
            "password": password,
            "transport": "gevent",
            "close_db": self._on_disconnect,
        }
        self.queue = queue

        self._connection = None
        self._channel = None
        self.lock = Semaphore()
        self.broken = False

    def disconnect(self):
        self.broken = True
        self._connection.disconnect()

    def _on_disconnect(self):
        self.broken = True

    def _on_channel_closed(self, channel):
        # Scrape the connection if our channel is closed.
        self.disconnect()

    def _open_connection(self):
        self._connection = HaighaConnection(**self._conn_kwargs)
        self._start_connection_loop()

    def _open_channel(self):
        # Open a channel and make sure we know if it gets closed
        self._channel = self._connection.channel()
        self._channel.add_close_listener(self._on_channel_closed)
        self._channel.queue.declare(self.queue, auto_delete=True)

    def _connection_loop(self):
    # The message pump needs to run for the connection to actually do something.
        while not self.broken:
            try:
                self._connection.read_frames()  # Pump
                gevent.sleep()  # Yield to other greenlets so they don't starve
            except Exception:
                # If the connection loop breaks, then we should stop using this conneciton!
                self.broken = True #TODO

    def _start_connection_loop(self):
        gevent.spawn(self._connection_loop)  # Power our connection

    def publish(self, key):
        # This expects that the channel is already open.
        msg = Message(key)
        self._channel.basic.publish(msg, "", self.queue)

    def dispatch(self, key):
        if self._channel is None:
            self._open_connection()
            self._open_channel()

        self.publish(key)


class RabbitMQDispatcher(Dispatcher):
    def __init__(self, host, port, vhost, user, password, queue):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.user = user
        self.password = password
        self.queue = queue

        self._pool = []


    def dispatch(self, key):
        for connection in self._pool:
            if connection.broken:
                continue

            if connection.lock.acquire(blocking=False):
                connection.dispatch(key)
                connection.lock.release()
                break
        else:
            connection = Connection(self.host, self.port, self.vhost, self.user, self.password, self.queue)
            connection.dispatch(key)
            self._pool.append(connection)

        # Clean up 10% of the time
        if random.random() < 0.1:
            self._pool = [connection for connection in self._pool if not connection.broken]


