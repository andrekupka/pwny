import itertools
import struct
from functools import wraps


WORD_SIZE_FORMAT_LOOKUP = {
    1: "B",
    2: "H",
    4: "I",
    8: "Q"
}


def pack_value(value, size=8, little_endian=True):
    pack_format = "<"
    if not little_endian:
        pack_format = ">"
    pack_format += WORD_SIZE_FORMAT_LOOKUP[size]
    return struct.pack(pack_format, value)


def encode_as_bytes(data):
    if isinstance(data, bytes):
        return data
    if not isinstance(data, str):
        data = str(data)
    return data.encode()


def encode_arg(index):
    def _encode_arg(f):
        def _inner(self, *args, **kwargs):
            before = args[0:index]
            arg = args[index]
            after = args[index+1:]
            if not isinstance(arg, bytes):
                arg = encode_as_bytes(arg)
            args = list(itertools.chain(before, [arg], after))
            return f(self, *args, **kwargs)
        return _inner
    return _encode_arg


def catch_all(f):
    return catch_all_with_error()(f)


def catch_all_with_error(error="An error occurred: ", print_exception=True):
    def _catch_all_with_error(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except Exception as e:
                if print_exception:
                    print("{}: {}".format(error, e))
                else:
                    print(error)
        return _inner
    return _catch_all_with_error
