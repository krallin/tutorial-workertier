#coding:utf-8
import argparse
import logging

from gevent import pywsgi, monkey; monkey.patch_all()
from gevent.event import Event

from smartcache.config import ConfigLoader
from smartcache.handler import Handler
from smartcache.consumer import Consumer


logging.basicConfig(level=logging.DEBUG)
DEFAULT_CONFIG_PATH = "config.ini"


def start_web(cache, dispatcher, config):
    handler = Handler(cache, dispatcher)
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), handler.handle_request)
    server.start()

def start_consumer(cache, dispatcher, config):
    consumer = Consumer(cache, dispatcher)
    consumer.start()

def main(role, config_path):
    config = ConfigLoader(config_path)
    cache = config.cache()
    dispatcher = config.dispatcher()
    ROLES[role](cache, dispatcher, config)

    # Just wait until the end of time now.
    event = Event()
    event.wait()


ROLES = {
    "web": start_web,
    "consumer": start_consumer
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser("smartcache")
    parser.add_argument("-c", "--config", default=DEFAULT_CONFIG_PATH, help="Path to a configuration file. "
                                                                            "Defaults to" + DEFAULT_CONFIG_PATH)
    parser.add_argument("role", help="The role we should run", choices=ROLES.keys())
    args = parser.parse_args()

    main(args.role, args.config)
