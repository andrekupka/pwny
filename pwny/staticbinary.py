from .binarybase import BinaryBase


class StaticBinary(BinaryBase):
    def __init__(self, name, offsets=None):
        super().__init__(name, offsets)

    def get_address(self, name, offset=0):
        address_offset = self._offsets.get(name)
        if address_offset is None:
            return None
        return address_offset + offset
