#coding:utf-8
import unittest

from workertier.consumer import Consumer
from workertier.backends.cache.memory import MemoryCache


class TestDispatcher(object):
    def __init__(self):
        self.started = 0

    def start_consumer(self, consume_message):
        self.started += 1
        self.consume_message = consume_message

    def simulate(self, message):
        self.consume_message(message)


class TestMessage(object):
    def __init__(self, body):
        self.body = body


class ConsumerTestCase(unittest.TestCase):
    def test_launch(self):
        n_consumers = 8
        dispatcher = TestDispatcher()
        consumer = Consumer(None, dispatcher, n_consumers)
        consumer.start()
        self.assertEqual(n_consumers, dispatcher.started)

    def test_message_received(self):
        store = {}

        dispatcher = TestDispatcher()
        consumer = Consumer(MemoryCache(store), dispatcher, 1)  # Don't need to start 5 non-processes...
        consumer.start()

        key, value = "mSg", "MsG"  #TODO: Our operation is a swapcase : l
        dispatcher.simulate(TestMessage(key))
        self.assertEqual(value, store.get(key))

