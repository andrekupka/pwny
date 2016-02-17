from .dynamicbinary import DynamicBinary


class BinaryStore:
    def __init__(self):
        self._binaries = dict()

    def add_binary(self, binary, name=None):
        if name is None:
            name = binary.get_name()
        # TODO check for duplicates
        self._binaries[name] = binary

    def get_binary(self, bin_name):
        return self._binaries.get(bin_name)

    def set_base_address(self, bin_name, base_address):
        binary = self._binaries[bin_name]
        if not isinstance(binary, DynamicBinary):
            raise Exception("Cannot set base address for non-dynamic binary.")
        binary.set_base_address(base_address)

    def get_address(self, name, bin_name, offset=0):
        binary = self._binaries.get(bin_name)
        if binary is None:
            raise Exception("No binary with name '{}' exists".format(bin_name))
        return binary.get_address(name, offset)
