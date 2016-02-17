from collections import OrderedDict
from .dynamicbinary import DynamicBinary


class BinaryStore:
    def __init__(self):
        self._binaries = OrderedDict()

    def add_binary(self, binary, name=None):
        if name is None:
            name = binary.get_name()
        if name in self._binaries:
            raise ValueError("Duplicated binary '{}'".format(name))
        self._binaries[name] = binary

    def get_binary(self, bin_name):
        return self._binaries.get(bin_name)

    def set_base_address(self, bin_name, base_address):
        binary = self._binaries[bin_name]
        if not isinstance(binary, DynamicBinary):
            raise ValueError("Cannot set base address for non-dynamic binary.")
        binary.set_base_address(base_address)

    def get_address(self, name, bin_name=None, offset=0):
        if bin_name is None:
            return self._search_all_binaries(name, offset)
        binary = self._binaries.get(bin_name)
        if binary is None:
            raise ValueError("No binary with name '{}' exists".format(bin_name))
        address = binary.get_address(name, offset)
        if address is None:
            raise ValueError("No symbol with name '{}' exists".format(name))
        return address

    def _search_all_binaries(self, name, offset):
        for binary in self._binaries.values():
            address = binary.get_address(name, offset)
            if address is not None:
                return address
        raise ValueError("No symbol with name '{}' exists".format(name))
