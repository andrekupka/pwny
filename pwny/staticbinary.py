from .binarybase import BinaryBase


class StaticBinary(BinaryBase):
    def __init__(self, name, offsets=None):
        super().__init__(name, offsets)

    def get_address(self, name, offset=0):
        return self._offsets[name] + offset
