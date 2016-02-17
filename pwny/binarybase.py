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

    def __getitem__(self, index):
        address = self._get_address(name, 0)
        if address is None:
            raise KeyError("'{}' cannot be looked up in {}"
                           .format(name, self._name))
        return address

    def add_offset(self, name, offset):
        if name in self._offsets:
            raise ValueError("Duplicated offset '{}'".format(name))
        self._offsets[name] = offset
