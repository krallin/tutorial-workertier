#coding:utf-8

class Cache(object):
    def get(self, key):
        raise NotImplementedError()

    def dispatch(self, key):
        raise NotImplementedError()