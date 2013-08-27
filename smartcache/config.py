#coding:utf-8
import ConfigParser


CONFIG_CLASS_OPT = "class"

class ConfigLoader(object):
    def __init__(self, *config_paths):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(config_paths)

    def _load_class(self, cls_path):
        module, cls = cls_path.rsplit(".", 1)

        try:
            _mod = __import__(module, fromlist=[cls])
        except ImportError:
            raise ImportError("Unable to import {0}".format(cls_path))
        else:
            return getattr(_mod, cls)

    def _get_object(self, section):
        cls_path = self.parser.get(section, CONFIG_CLASS_OPT)  # May raise an error
        cls = self._load_class(cls_path)
        kwargs = dict(((k, v) for k, v in self.parser.items(section) if k != CONFIG_CLASS_OPT))
        kwargs = dict((k, int(v) if v.isdigit() else v) for k, v in kwargs.items())
        return cls(**kwargs)

    def cache(self):
        return self._get_object("cache")

    def dispatcher(self):
        return self._get_object("dispatcher")
