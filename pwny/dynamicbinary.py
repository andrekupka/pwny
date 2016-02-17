from .binarybase import BinaryBase


class DynamicBinary(BinaryBase):
    def __init__(self, name, offsets=None, base_address=None):
        super().__init__(name, offsets)
        self._base_address = base_address

    def set_base_address(self, base_address):
        self._base_address = base_address

    def get_address(self, name, offset=0):
        if self._base_address is None:
            raise Exception("no base address has been set")
        address_offset = self._offsets.get(name)
        if address_offset is None:
            return None
        return address_offset + self._base_address + offset
