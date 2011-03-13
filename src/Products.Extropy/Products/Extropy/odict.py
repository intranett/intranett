# util.py
# Copyright (C) 2005,2006 Michael Bayer mike_mp@zzzcomputing.com
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

class OrderedDict(dict):
    """A Dictionary that returns keys/values/items in the order they were added"""
    def __new__(cls, d=None, **kwargs):
        instance = super(OrderedDict, cls).__new__(cls)
        instance._list = []
        instance.update(d, **kwargs)
        return instance
    def keys(self):
        return list(self._list)
    def clear(self):
        self._list = []
        dict.clear(self)
    def update(self, d=None, **kwargs):
        # d can be a dict or sequence of keys/values
        if d:
            if hasattr(d, 'iteritems'):
                seq = d.iteritems()
            else:
                seq = d
            for key, value in seq:
                self.__setitem__(key, value)
        if kwargs:
            self.update(kwargs)
    def setdefault(self, key, value):
        if not self.has_key(key):
            self.__setitem__(key, value)
            return value
        else:
            return self.__getitem__(key)
    def values(self):
        return [self[key] for key in self._list]
    def __iter__(self):
        return iter(self._list)
    def itervalues(self):
        return iter([self[key] for key in self._list])
    def iterkeys(self): 
        return self.__iter__()
    def iteritems(self):
        return iter([(key, self[key]) for key in self.keys()])
    def __delitem__(self, key):
        try:
            del self._list[self._list.index(key)]
        except ValueError:
            raise KeyError(key)
        dict.__delitem__(self, key)
    def __setitem__(self, key, object):
        if not self.has_key(key):
            self._list.append(key)
        dict.__setitem__(self, key, object)
    def __getitem__(self, key):
        return dict.__getitem__(self, key)
