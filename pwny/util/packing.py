from struct import pack, unpack


def _get_format(form, little_endian):
    if little_endian:
        return "<" + form
    return ">" + form


def p8(value):
    return pack("B", value)


def p16(value, little_endian=True):
    return pack(_get_format("H", little_endian), value)


def p32(value, little_endian=True):
    return pack(_get_format("I", little_endian), value)


def p64(value, little_endian=True):
    return pack(_get_format("Q", little_endian), value)


def u8(value):
    return unpack("B", value)


def u16(value, little_endian=True):
    return unpack(_get_format("H", little_endian), value)


def u32(value, little_endian=True):
    return unpack(_get_format("I", little_endian), value)


def u64(value, little_endian=True):
    return unpack(_get_format("Q", little_endian), value)
