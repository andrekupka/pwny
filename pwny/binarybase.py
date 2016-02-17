from abc import ABCMeta, abstractmethod


class BinaryBase(metaclass=ABCMeta):
    def __init__(self, name, offsets=None):
        self._name = name
        if offsets:
            self._offsets = offsets.copy()
        else:
            self._offsets = dict()

    def get_name(self):
        return self._name

    @abstractmethod
    def get_address(self, name, offset=0):
        pass

    def __setitem__(self, index, value):
        self.add_offset(index, value)

    def add_offset(self, name, offset):
        # TODO check for duplicated offsets?
        self._offsets[name] = offset
