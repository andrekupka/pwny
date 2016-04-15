from .util import encode_as_bytes, pack_value


class RopChain:
    def __init__(self, pwny):
        """Constructor.

        :param pwny.Pwny pwny: the parent Pwny that has created the chain
        """
        self._pwny = pwny
        self._chain = list()

    def get_pwny(self):
        """
        Returns the parent pwny.
        """
        return self._pwny

    def append(self, obj):
        """Appends a generic object to the rop chain and tries to convert is to
        byte string.

        Long.

        :param object obj: the generic object that is to be added
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

    def newline(self):
        """
        Adds a newline to the chain.
        """
        self.byte(0xa)

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
        self._chain.append(self._pack_value(value, size, little_endian))

    def addr(self, name, bin_name=None, size=None, little_endian=None):
        self._chain.append(lambda: self._pack_addr(name, bin_name, size,
                                                   little_endian))

    def _pack_addr(self, name, bin_name, size, little_endian):
        address = self._pwny._binary_store.get_address(name, bin_name)
        return self._pack_value(address, size, little_endian)

    def _pack_value(self, value, size, little_endian):
        size = size or self._pwny._word_size
        little_endian = little_endian or self._pwny._little_endian
        return pack_value(value, size, little_endian)

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
