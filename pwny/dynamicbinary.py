from .binarybase import BinaryBase


class DynamicBinary(BinaryBase):
    def __init__(self, name, offsets=None, base_address=None):
        """
        Constructor.

        :param name: the binary's name
        :type name: str
        :param offsets: initial offsets that are stored into the binary
        :type offsets: dict or None
        :param base_address: the binary's base address in virtual memory
        :type base_address: int or None
        """
        super().__init__(name, offsets)
        self._base_address = base_address

    def set_base_address(self, base_address):
        """
        Sets the base address of the binary. The base address is the start
        address where this binary has been mapped into virtual memory.

        :param base_address: the base address
        :type base_address: int
        """
        self._base_address = base_address

    def get_address(self, name, offset=0):
        """
        TODO inherit doc
        """
        if self._base_address is None:
            raise Exception("no base address has been set")
        address_offset = self._offsets.get(name)
        if address_offset is None:
            return None
        return address_offset + self._base_address + offset
