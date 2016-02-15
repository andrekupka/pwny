from .util import encode_as_bytes, pack_value


class RopChain:
    def __init__(self, pwny):
        self._pwny = pwny
        self._chain = list()

    def get_pwny(self):
        """
        Returns the parent pwny.
        """
        return self._pwny

    def append(self, obj):
        """
        Appends a generic object to the rop chain and tries to convert is to
        byte string.
        """
        self._chain.append(obj)

    def pad(self, length, scale=1, value=b"_"):
        """
        Pads the chain with length multiplied by scale times the given value.
        """
        if isinstance(value, int):
            value = pack_value(value, 1)
        self._chain.append(length * scale * value)

    def byte(self, value):
        """
        Adds a byte to the chain.
        """
        self.value(value, size=1)

    def word(self, value, little_endian=None):
        """
        Adds a word (2 bytes) to the chain.
        """
        self.value(value, size=2, little_endian=little_endian)

    def dword(self, value, little_endian=None):
        """
        Adds a double word (4 bytes) to the chain.
        """
        self.value(value, size=4, little_endian=little_endian)

    def qword(self, value, little_endian=None):
        """
        Adds a quad word (8 bytes) to the chain.
        """
        self.value(value, size=8, little_endian=little_endian)

    def value(self, value, size=None, little_endian=None):
        """
        Adds a value to the chain. The value is packed into the given size
        bytes with the given endianess. If none is specified the word size and
        endianess of the parent Pwny is used.
        """
        size = size or self._pwny._word_size
        little_endian = little_endian or self._pwny._little_endian
        self._chain.append(pack_value(value, size))

    def serialize(self):
        """
        Serializes the chain into a byte string.
        """
        serialized = b""
        for part in self._chain:
            if callable(part):
                part = part()
            serialized += encode_as_bytes(part)
        return serialized

    def send(self):
        """
        Sends the serialized chain to the remote host using the parent pwny.
        """
        self._pwny.send(self.serialize())
