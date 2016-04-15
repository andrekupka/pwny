from abc import ABCMeta, abstractmethod


class BinaryBase(metaclass=ABCMeta):
    def __init__(self, name, offsets=None):
        """
        Constructor.

        :param name: the binary's name
        :type name: str
        :param offsets: initial offsets that are stored into the binary
        :type offsets:  dict or None
        """
        self._name = name
        if offsets:
            self._offsets = offsets.copy()
        else:
            self._offsets = dict()

    def get_name(self):
        """
        Returns the name.
        """
        return self._name

    @abstractmethod
    def get_address(self, name, offset=0):
        """
        Resolves the address of the symbol with the given name and adds the
        given offset.

        :param name: the symbol's name
        :type name: str
        :param offset: an offset that is added to the returned address
        :type offset: int
        """
        pass

    def __setitem__(self, name, offset):
        """
        Sets the offset of the symbol with the given name.

        :param name: the symbol's name
        :type name: str
        :param offset: the offset of the symbol within the binary
        :type offset: int
        """
        self.add_offset(name, offset)

    def __getitem__(self, name):
        """
        Resolves the address of the symbol with the given name.

        :param name: the symbol's name
        :type name: str
        :raises KeyError:
        """
        address = self._get_address(name, 0)
        if address is None:
            raise KeyError("'{}' cannot be looked up in {}"
                           .format(name, self._name))
        return address

    def add_offset(self, name, offset):
        """
        Adds the offset of the symbol with the given name.

        :param name: the symbol's name
        :type name: str
        :param offset: the offset of the symbol within the binary
        :type offset: int
        """
        if name in self._offsets:
            raise ValueError("Duplicated offset '{}'".format(name))
        self._offsets[name] = offset
