def parse_pointer_leak(leaked_data):
    if isinstance(leaked_data, bytes):
        leaked_data = leaked_data.decode()

    leaked_data = leaked_data.replace("(nil)", "0x0")
    return list(map(lambda addr: int(addr, 16), parts))
