#coding:utf-8
class Backend(object):
    def __init__(self, cache, dispatcher):
        """
        :type cache: :class:`smartcache.backends.cache.Cache`
        :type dispatcher: :class:`smartcache.backends.dispatcher.Dispatcher`
        """
        self._cache = cache
        self._dispatcher = dispatcher

    def get(self, key):
        value = self._cache.get(key)
        if value is None:
            self._dispatcher.dispatch(key)
        return value

