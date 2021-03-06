#coding:utf-8
import logging

from workertier.backends import InvalidKey, BackendUnavailable


logger = logging.getLogger(__name__)


class Handler(object):
    def __init__(self, cache, dispatcher):
        self.cache = cache
        self.dispatcher = dispatcher

    def handle_request(self, env, start_response):
        method = env["REQUEST_METHOD"]
        url = env["PATH_INFO"]

        logger.debug("Received request: %s %s", method, url)

        if method not in ("HEAD", "GET"):
            start_response("405 METHOD NOT ALLOWED", [])
            return

        if not url.startswith("/") or url == "/":
            start_response("404 Not Found", [])
            return

        key = url[1:]

        try:
            value = self.cache.get(key)
            # Note: This wouldn"t make sense for an HA app, but we"re just trying to do a POC here,
            # so we'll appreciate the debug info in case our dispatcher dies.
            if value is None:
                self.dispatcher.dispatch(key)
        except InvalidKey:
            start_response("400 Bad Request", [])
            logger.warning("Invalid key: %s", key)
            return
        except BackendUnavailable:
            start_response("503 Service Unavailable", [])
            logger.warning("Backend unavailable")
            return

        if value is None:
            start_response("203 Non-Authoritative Information", [])
            return

        start_response("200 OK", [("Content-Type", "text/plain")])
        yield value
        yield "\n"
